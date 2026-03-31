from contextlib import asynccontextmanager
from typing import AsyncIterator

from amqtt.client import ClientConfig, MQTTClient
from amqtt.contexts import ConnectionConfig
from loguru import logger

from app.settings.hono import HonoConfig


class Hono:
    def __init__(self, config: HonoConfig) -> None:
        self.config = config
        logger.debug("Hono uri: {}", config.get_uri())
        self._mqttc = MQTTClient(
            config=ClientConfig(
                reconnect_retries=-1,
                check_hostname=False,
                connection=ConnectionConfig(
                    cafile=config.cafile,
                    cadata=config.cadata,
                    uri=config.get_uri(),
                ),
            )
        )

    @property
    @asynccontextmanager
    async def client(self) -> AsyncIterator[None]:
        logger.debug("Connections return code: {}", await self._mqttc.connect())

        yield

        await self._mqttc.disconnect()

    async def send(self, payload: bytes) -> None:
        await self._mqttc.publish(self.config.topic, payload)
