from pydantic import BaseModel

from app.models.level_ams import geotechnical_asset


class Attributes(geotechnical_asset.GeotechnicalAsset):
    instrumentList: list[str]


class GeotechnicalAssetDitto(BaseModel):
    policyId: str
    attributes: Attributes
