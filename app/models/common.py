from typing import Annotated, TypeVar, Union

from pydantic import BaseModel, Field, NonNegativeInt
from pydantic import JsonValue as JV
from pyproj import Transformer

type Lon = Annotated[float, Field(ge=-180, le=180)]
type Lat = Annotated[float, Field(ge=-90, le=90)]

type NonEmptyStr = Annotated[str, Field(min_length=1)]

type JsonValue = Union[JV, BaseModel]


class Coordinates(BaseModel):
    latitude: float
    longitude: float

    @classmethod
    def from_etrs89_tm06(cls, x: float, y: float):
        lat, lon = Transformer.from_crs(3763, 4326).transform(x, y)
        return cls(latitude=lat, longitude=lon)


T = TypeVar("T", bound=BaseModel)


class PaginationWrapper[T](BaseModel):
    items: list[T]
    pageIndex: NonNegativeInt
    totalPages: NonNegativeInt
    pageSize: NonNegativeInt
    totalCount: NonNegativeInt
    hasPreviousPage: bool
    hasNextPage: bool


class ValueNamePair(BaseModel):
    value: str
    name: str
