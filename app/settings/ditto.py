from pathlib import Path
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from app.models.common import NonEmptyStr


class DittoConfig(BaseModel):
    default_policy: NonEmptyStr = "dt4mob:default"

    username: Optional[str] = None
    password: Optional[str] = None

    base_url: AnyHttpUrl = AnyHttpUrl("http://localhost/api/2")

    cafile: Optional[Path] = None
    cadata: Optional[str] = None
