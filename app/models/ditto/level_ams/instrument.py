from typing import Dict, List, Optional

from pydantic import BaseModel, Field, RootModel

from app.models.common import Coordinates, MeasurementState, NonEmptyStr
from app.models.level_ams import instrument, parameter


class ETRS89_TM06(BaseModel):
    x: float
    y: float


class Attributes(instrument.Instrument):
    coordinates: Coordinates
    geotile: int
    parametros: List[instrument.Parameter] = Field(exclude=True)
    dashboardUrl: Optional[str] = None


class Property(instrument.Parameter):
    latestValue: Optional[parameter.Parameter]
    state: MeasurementState


class Properties(BaseModel):
    properties: Property


Features = RootModel[Dict[NonEmptyStr, Properties]]


class InstrumentDitto(BaseModel):
    policyId: str
    attributes: Attributes
    features: Features
