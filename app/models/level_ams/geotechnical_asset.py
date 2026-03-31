from pydantic import BaseModel, ConfigDict

from app.models.common import Lat, Lon, ValueNamePair


class GeotechnicalAssetSummary(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str


class GeotechnicalAsset(BaseModel):
    id: str
    matricula: str
    localizacao: str
    tipoActivo: ValueNamePair
    latitude: Lat
    longitude: Lon
    indiceCondicaoAtual: float
    indiceFiabilidade: float
    altura: float
    extensao: float
    inclinacaoGraus: int
    pkExploracaoInicial: int
    pkExploracaoFinal: int
    pkProjectInicial: int
    pkProjectFinal: int
