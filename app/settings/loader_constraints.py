from typing import Annotated, Optional, Set

from pydantic.v1 import BaseModel, Field, validator


class LoaderConstraints(BaseModel):
    geo_asset_id: Annotated[
        Optional[str],
        Field(
            description="If set, the loader will only load the geotechnical asset with the provided ID."
        ),
    ]

    instrument_ids: Annotated[
        Optional[Set[str]],
        Field(
            description="If set, the loader will only load the information from the instrument with the provided ID. Note that --geo-asset-id must also be set to use this option."
        ),
    ]

    @validator("instrument_ids")
    def check_geo_asset_id_is_set(cls, v, values):
        if v and not values["geo_asset_id"]:
            raise ValueError("INSTRUMENT_IDS set without setting GEO_ASSET_ID")
        return v
