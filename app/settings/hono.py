from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from app.models.common import NonEmptyStr


class HonoConfig(BaseModel):
    host: str = "127.0.0.1"
    port: Optional[int] = None

    device: Optional[str] = None
    tenant: Optional[str] = None
    password: Optional[str] = None

    cafile: Optional[Path] = None
    certfile: Optional[Path] = None
    keyfile: Optional[Path] = None

    topic: NonEmptyStr = "telemetry"

    @property
    def username(self) -> Optional[str]:
        if self.device and self.tenant:
            return f"{self.device}@{self.tenant}"

    def get_uri(self) -> str:
        uri: list[str] = ["mqtts://"]
        if self.username is not None:
            uri.append(self.username)
            if self.password is not None:
                uri.append(f":{self.password}")
            uri.append("@")

        uri.append(self.host)
        if self.port is not None:
            uri.append(f":{self.port}")

        return "".join(uri)
