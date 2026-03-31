from datetime import datetime
from enum import StrEnum
from typing import Dict

from pydantic import BaseModel, JsonValue


class Action(StrEnum):
    modified = "modified"
    created = "created"
    deleted = "deleted"
    merged = "merged"


type Value = Dict[str, JsonValue]


class Item(BaseModel):
    time: datetime
    thing_id: str
    action: Action
    revision: int = 1
    path: str
    value: Value


class Event(BaseModel):
    events: list[Item]
