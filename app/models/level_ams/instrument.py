import csv
from pathlib import Path
from typing import List, Optional, Self

from pydantic import BaseModel, RootModel

from app.models.common import ValueNamePair


class Limit(BaseModel):
    criterio: ValueNamePair
    valor: float
    variacaoAbsoluta: float


class Parameter(BaseModel):
    parametroNome: str
    parametroChave: str
    unidades: str
    limiteAlerta: Optional[Limit]
    limiteAlarme: Optional[Limit]


class Instrument(BaseModel):
    instrumentoId: str
    tipoInstrumento: ValueNamePair
    matricula: str
    pkInicial: int
    parametros: List[Parameter]


Instruments = RootModel[List[Instrument]]


class InstrumentCoordinate(BaseModel):
    matricula: str
    x: float
    y: float
    z: float

    @classmethod
    def load_from_csv(cls, filepath: Path) -> dict[str, Self]:
        with filepath.open("r") as f:
            reader = csv.DictReader(f)
            return {row["matricula"]: cls.model_validate(row) for row in reader}
