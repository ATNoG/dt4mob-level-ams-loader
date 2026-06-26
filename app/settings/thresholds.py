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

    def check(self, latestValue: float, earliestValue: float) -> bool:
        match self.threshold_type:
            case ThresholdType.GT:
                return latestValue > self.value
            case ThresholdType.LT:
                return latestValue < self.value
            case ThresholdType.DELTA:
                return abs(latestValue - earliestValue) > self.value


class Thresholds(BaseModel):
    parameter_types: set[str]
    alert: Threshold
    alarm: Threshold

    def get_measurement_state(
        self, parameter_key: str, latestValue: float, earliestValue: float
    ) -> MeasurementState:
        if parameter_key.rstrip("0123456789") not in self.parameter_types:
            return MeasurementState.OK

        if self.alarm.check(latestValue, earliestValue):
            return MeasurementState.ALARM

        if self.alert.check(latestValue, earliestValue):
            return MeasurementState.ALERT

        return MeasurementState.OK


InstrumentThresholds = RootModel[dict[str, Thresholds]]
InstrumentTypeThresholds = RootModel[dict[InstrumentType, Thresholds]]
