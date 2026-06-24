from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from app.models.common import NonEmptyStr


class HonoConfig(BaseModel):
    host: str = "127.0.0.1"
    port: Optional[int] = None

    cafile: Path = Path("./ca.crt")
    certfile: Path = Path("./crt.pem")
    keyfile: Path = Path("./key.pem")

    topic: NonEmptyStr = "telemetry"

    def get_uri(self) -> str:
        uri: list[str] = [f"mqtts://{self.host}"]
        if self.port is not None:
            uri.append(f":{self.port}")

        return "".join(uri)
