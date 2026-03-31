from asyncio import Task, TaskGroup
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import AsyncIterator, Optional

import httpx
from loguru import logger

from app.dependencies.ditto_client import get_ditto_client
from app.dependencies.history_client import get_history_client
from app.hono_connection import Hono
from app.models.common import Coordinates, PaginationWrapper
from app.models.ditto import (
    Channel,
    CommandAction,
    Criterion,
    DittoProtocolEnvelope,
    Group,
    ModifiedTime,
    Topic,
)
from app.models.ditto.level_ams import geotechnical_asset
from app.models.ditto.level_ams import instrument as ditto_instrument
from app.models.history import event
from app.models.level_ams import parameter
from app.models.level_ams.geotechnical_asset import GeotechnicalAsset
from app.models.level_ams.instrument import (
    Instrument,
    InstrumentCoordinate,
    Instruments,
    Parameter,
)
from app.models.level_ams.parameter import Parameter as ParameterValue
from app.settings import settings
from app.settings.loader import LoaderConfig
from app.settings.loader_constraints import LoaderConstraints


class LevelAMSLoader:
    def __init__(
        self, hono: Hono, config: LoaderConfig, constraints: LoaderConstraints
    ) -> None:
        self.config = config
        self.constraints = constraints
        self.ditto_client = get_ditto_client()
        self.history_client = None
        if settings.history.enabled:
            self.history_client = get_history_client()

        auth_headers = {
            "Authorization": f"Bearer {config.get_jwt(httpx.Client(base_url=config.get_url()))}"
        }
        self.http_client = httpx.AsyncClient(
            base_url=f"{config.get_url()}/v1",
            timeout=config.http_timeout,
            headers=auth_headers,
        )
        self.hono = hono

    @property
    @asynccontextmanager
    async def _resources(self) -> AsyncIterator[None]:
        async with self.http_client, self.hono.client:
            yield

    async def _handle_parameter_history(
        self, geo_asset_id: str, instrument_id: str, parameter_key: str
    ) -> list[event.Item]:
        tomorrow = (datetime.now(tz=timezone.utc) + timedelta(days=1)).isoformat()
        query_params = {"StartDate": "1970-01-01", "EndDate": tomorrow, "Page": 1}
        res = await self.http_client.get(
            f"/activos-geotecnicos/{geo_asset_id}/instrumento/{instrument_id}/parametro/{parameter_key}/data",
            params=query_params,
        )

        first_page = PaginationWrapper[parameter.Parameter].model_validate_json(
            res.content
        )
        tasks: list[Task[httpx.Response]] = []
        chunk_size = 5
        page_ranges = [
            range(i, min(i + chunk_size, first_page.totalPages + 1))
            for i in range(1, first_page.totalPages + 1, chunk_size)
        ]
        for page_chunk in page_ranges:
            async with TaskGroup() as tg:
                for page_idx in page_chunk:
                    query_params = {
                        "StartDate": "1970-01-01",
                        "EndDate": tomorrow,
                        "Page": page_idx,
                    }
                    tasks.append(
                        tg.create_task(
                            self.http_client.get(
                                f"/activos-geotecnicos/{geo_asset_id}/instrumento/{instrument_id}/parametro/{parameter_key}/data",
                                params=query_params,
                            )
                        )
                    )

        event_items: list[event.Item] = []
        for task in tasks:
            res = task.result()
            if not res.is_success:
                raise RuntimeError("Request failed during history processing")

            page = PaginationWrapper[parameter.Parameter].model_validate_json(
                res.content
            )

            event_items.extend(
                event.Item(
                    time=item.timestamp,
                    thing_id=f"{self.hono.config.device}:{geo_asset_id}.instrument.{instrument_id}",
                    action=event.Action.modified,
                    path=f"/features/{parameter_key}/properties/latestValue",
                    value=item.model_dump(mode="json"),
                )
                for item in page.items
            )
        return event_items

    async def _handle_parameter(
        self, geo_asset_id: str, instrument_id: str, parameter_key: str
    ) -> Optional[ParameterValue]:
        hour_before_last_update = (
            await ModifiedTime.get_time(
                self.ditto_client,
                self.hono.config.device,
                geo_asset_id,
                instrument_id,
            )
            - timedelta(hours=1)
        ).isoformat()
        tomorrow = (datetime.now(tz=timezone.utc) + timedelta(days=1)).isoformat()
        query_params = {
            "StartDate": hour_before_last_update,
            "EndDate": tomorrow,
        }
        res = await self.http_client.get(
            f"/activos-geotecnicos/{geo_asset_id}/instrumento/{instrument_id}/parametro/{parameter_key}/data",
            params=query_params,
        )

        first_page = PaginationWrapper[parameter.Parameter].model_validate_json(
            res.content
        )
        return first_page.items[0] if len(first_page.items) > 0 else None

    async def _handle_instrument(
        self,
        instrument: Instrument,
        geo_asset_id: str,
        instrument_coords: InstrumentCoordinate,
    ) -> None:
        tasks: list[tuple[Parameter, Task[Optional[ParameterValue]]]] = []
        logger.info("Started handling instrument: {}", instrument.instrumentoId)
        chunk_size = self.config.parameters_chunk_size
        param_chunks = [
            instrument.parametros[i : i + chunk_size]
            for i in range(0, len(instrument.parametros), chunk_size)
        ]
        for chunk in param_chunks:
            async with TaskGroup() as tg:
                for parameter in chunk:
                    tasks.append(
                        (
                            parameter,
                            tg.create_task(
                                self._handle_parameter(
                                    geo_asset_id,
                                    instrument.instrumentoId,
                                    parameter.parametroChave,
                                )
                            ),
                        )
                    )

        msg = DittoProtocolEnvelope(
            topic=Topic(
                namespace=self.hono.config.device,
                thingName=f"{geo_asset_id}.instrument.{instrument.instrumentoId}",
                group=Group.THING,
                channel=Channel.TWIN,
                criterion=Criterion.COMMAND,
                action=CommandAction.CREATE,
            ),
            value=ditto_instrument.InstrumentDitto(
                policyId=settings.ditto.default_policy,
                attributes=ditto_instrument.Attributes(
                    **instrument.model_dump(),
                    coordinates=Coordinates.from_etrs89_tm06(
                        instrument_coords.x, instrument_coords.y
                    ),
                ),
                features=ditto_instrument.Features(dict()),
            ).model_dump(mode="json"),
        )

        await self.hono.send(msg.model_dump_json(exclude_none=True).encode())

        for parameter, task in tasks:
            msg = DittoProtocolEnvelope(
                topic=Topic(
                    namespace=self.hono.config.device,
                    thingName=f"{geo_asset_id}.instrument.{instrument.instrumentoId}",
                    group=Group.THING,
                    channel=Channel.TWIN,
                    criterion=Criterion.COMMAND,
                    action=CommandAction.MODIFY,
                ),
                path=f"/features/{parameter.parametroChave}",
                value=ditto_instrument.Properties(
                    properties=ditto_instrument.Property(
                        **parameter.model_dump(), latestValue=task.result()
                    )
                ).model_dump(mode="json"),
            )
            await self.hono.send(msg.model_dump_json(exclude_none=True).encode())

        logger.info("Finished handling instrument: {}", instrument.instrumentoId)

        if not settings.history.enabled or not self.history_client:
            return

        logger.info(
            "Started loading history for instrument: {}", instrument.instrumentoId
        )

        history_tasks: list[Task[list[event.Item]]] = []
        if settings.history.enabled:
            for chunk in param_chunks:
                async with TaskGroup() as tg:
                    for parameter in chunk:
                        history_tasks.append(
                            tg.create_task(
                                self._handle_parameter_history(
                                    geo_asset_id,
                                    instrument.instrumentoId,
                                    parameter.parametroChave,
                                )
                            ),
                        )
        history_event = event.Event(events=[])
        for task in history_tasks:
            history_event.events.extend(task.result())

        print("{}MB", len(history_event.model_dump_json()) / 2 ** (10 * 2))
        logger.debug(
            "Events Response Status Code: {}",
            (
                await self.history_client.post(
                    "/events", json=history_event.model_dump(mode="json")
                )
            ).status_code,
        )

        logger.info(
            "Finished loading history for instrument: {}", instrument.instrumentoId
        )

    async def _handle_instruments(
        self, instruments: list[Instrument], geo_asset_id: str
    ) -> None:
        instrument_coords = InstrumentCoordinate.load_from_csv(
            settings.loader.instrument_coords_file
        )

        chunk_size = self.config.instruments_chunk_size
        instrument_chunks = [
            instruments[i : i + chunk_size]
            for i in range(0, len(instruments), chunk_size)
        ]
        for chunk in instrument_chunks:
            async with TaskGroup() as tg:
                for instrument in chunk:
                    tg.create_task(
                        self._handle_instrument(
                            instrument,
                            geo_asset_id,
                            instrument_coords[instrument.matricula],
                        )
                    )

    async def _handle_geo_asset_id(self, id: str) -> None:
        async with TaskGroup() as tg:
            logger.debug("Request geo asset details")
            geo_asset_details_task = tg.create_task(
                self.http_client.get(f"/activos-geotecnicos/{id}")
            )
            logger.debug("Request geo asset sensor-list")
            instrument_list_task = tg.create_task(
                self.http_client.get(f"/activos-geotecnicos/{id}/sensor-list")
            )

        geo_asset_res, instrument_list_res = (
            geo_asset_details_task.result(),
            instrument_list_task.result(),
        )

        if not geo_asset_res.is_success:
            logger.error("{}", geo_asset_res)
            raise RuntimeError(f"Failed getting details for id: {id}")
        logger.trace("Geo asset response body: {body}", body=geo_asset_res.content)
        geo_asset = GeotechnicalAsset.model_validate_json(geo_asset_res.content)

        if not instrument_list_res.is_success:
            logger.error("{}", instrument_list_res)
            raise RuntimeError(f"Failed getting sensor list for id: {id}")
        logger.trace(
            "Instrument list response body: {body}", body=instrument_list_res.content
        )
        instruments = Instruments.model_validate_json(instrument_list_res.content)

        geo_asset_attributes = geotechnical_asset.Attributes(
            **geo_asset.model_dump(),
            instrumentList=[
                f"{id}.instrument.{instrument.instrumentoId}"
                for instrument in instruments.root
            ],
        )
        msg = DittoProtocolEnvelope(
            topic=Topic(
                namespace=self.hono.config.device,
                thingName=geo_asset.id,
                group=Group.THING,
                channel=Channel.TWIN,
                criterion=Criterion.COMMAND,
                action=CommandAction.CREATE,
            ),
            value=geotechnical_asset.GeotechnicalAssetDitto(
                policyId=settings.ditto.default_policy, attributes=geo_asset_attributes
            ).model_dump(mode="json"),
        )
        if self.constraints.instrument_ids:
            instruments.root = [
                instrument
                for instrument in instruments.root
                if instrument.instrumentoId in self.constraints.instrument_ids
            ]
        async with TaskGroup() as tg:
            tg.create_task(
                self.hono.send(msg.model_dump_json(exclude_none=True).encode())
            )
            tg.create_task(self._handle_instruments(instruments.root, id))

    async def _handle_all_geo_assets(self):
        raise RuntimeError(
            "Handle all geo assets is not implement, please provide a GEO_ASSET_ID."
        )

    async def run(self) -> None:
        logger.info("Starting loader")
        async with self._resources:
            if self.constraints.geo_asset_id:
                await self._handle_geo_asset_id(self.constraints.geo_asset_id)
            else:
                await self._handle_all_geo_assets()
        logger.success("Loader finished successfully")
