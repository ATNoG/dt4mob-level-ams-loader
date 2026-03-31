from typing import Dict, List, Optional

from pydantic import BaseModel, Field, RootModel

from app.models.common import Coordinates, NonEmptyStr
from app.models.level_ams import instrument, parameter


class ETRS89_TM06(BaseModel):
    x: float
    y: float


class Attributes(instrument.Instrument):
    coordinates: Coordinates
    parametros: List[instrument.Parameter] = Field(exclude=True)


class Property(instrument.Parameter):
    latestValue: Optional[parameter.Parameter]


class Properties(BaseModel):
    properties: Property


Features = RootModel[Dict[NonEmptyStr, Properties]]


class InstrumentDitto(BaseModel):
    policyId: str
    attributes: Attributes
    features: Features
