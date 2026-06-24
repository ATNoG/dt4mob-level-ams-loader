import urllib.parse
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from app.models.common import InstrumentType


class DashboardConfig(BaseModel):
    inclinometer_base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1")
    inclinometer_query_param: str = "var-instrument_id"

    load_cell_base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1")
    load_cell_query_param: str = "var-instrument_id"

    def build_url(
        self,
        instrument_type: str,
        namespace: str,
        subject: str,
        geo_asset_id: str,
        matricula: str,
    ) -> Optional[str]:
        match instrument_type:
            case InstrumentType.INCLINOMETER.value:
                base_url = str(self.inclinometer_base_url).rstrip("/")
                query_param = self.inclinometer_query_param

            case InstrumentType.LOAD_CELL.value:
                base_url = str(self.load_cell_base_url).rstrip("/")
                query_param = self.load_cell_query_param

            case _:
                return

        url_parts = list(urllib.parse.urlparse(base_url))

        # NOTE: url_parts is a list where the fourth index always corresponds to the query params
        query_params = urllib.parse.parse_qsl(url_parts[4])
        query_params.append(
            (
                query_param,
                f"{namespace}:{subject}:{geo_asset_id}.instrument.{matricula}",
            )
        )
        url_parts[4] = urllib.parse.urlencode(query_params)

        return urllib.parse.urlunparse(url_parts)
