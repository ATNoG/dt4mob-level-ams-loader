from enum import StrEnum

from pydantic import BaseModel, RootModel

from app.models.common import InstrumentType, MeasurementState


class ThresholdType(StrEnum):
    LT = "LT"
    GT = "GT"
    DELTA = "DELTA"


class Threshold(BaseModel):
    threshold_type: ThresholdType
    value: float

    def check(self, value: float) -> bool:
        match self.threshold_type:
            case ThresholdType.GT:
                return value > self.value
            case ThresholdType.LT:
                return value < self.value
            case ThresholdType.DELTA:
                return abs(value) > self.value


class Thresholds(BaseModel):
    parameter_types: set[str]
    alert: Threshold
    alarm: Threshold

    def get_measurement_state(
        self, parameter_key: str, value: float
    ) -> MeasurementState:
        if parameter_key.rstrip("0123456789") not in self.parameter_types:
            return MeasurementState.OK

        if self.alarm.check(value):
            return MeasurementState.ALARM

        if self.alert.check(value):
            return MeasurementState.ALERT

        return MeasurementState.OK


InstrumentThresholds = RootModel[dict[str, Thresholds]]
InstrumentTypeThresholds = RootModel[dict[InstrumentType, Thresholds]]
