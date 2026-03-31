from datetime import datetime

from pydantic import BaseModel


class Parameter(BaseModel):
    timestamp: datetime
    valor: float
