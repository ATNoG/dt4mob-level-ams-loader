from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from app.models.common import NonEmptyStr


class HonoConfig(BaseModel):
    cafile: Optional[Path] = None
    cadata: Optional[str] = None
    secure: bool = False

    host: str = "127.0.0.1"
    port: Optional[int] = None

    device: NonEmptyStr = "device"
    tenant: NonEmptyStr = "tenant"
    password: NonEmptyStr = "changme"

    topic: NonEmptyStr = "telemetry"

    def get_uri(self) -> str:
        uri: list[str] = ["mqtt"]
        if self.secure:
            uri.append("s")
        uri.append(f"://{self.device}@{self.tenant}:{self.password}@{self.host}")
        if self.port is not None:
            uri.append(f":{self.port}")

        return "".join(uri)
