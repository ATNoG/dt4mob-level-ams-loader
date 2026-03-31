from pathlib import Path
from typing import Annotated, Optional

import httpx
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, PositiveInt


class Credentials(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    token: str


class LoaderConfig(BaseModel):
    jwt: Optional[str] = None
    base_url: AnyHttpUrl = AnyHttpUrl("http://localhost")

    credentials: Optional[Credentials] = None

    http_timeout: Optional[float] = 30

    start_page_idx: PositiveInt = 1

    instrument_coords_file: Path = Path("instrument_coords.csv")

    parameters_chunk_size: Annotated[
        PositiveInt,
        Field(description="Number of parameters handled in parallel per instrument"),
    ] = 10
    instruments_chunk_size: Annotated[
        PositiveInt,
        Field(description="Number of instruments handled in parallel"),
    ] = 10

    def get_url(self, path: Optional[str] = None) -> str:
        base_url = str(self.base_url).rstrip("/")
        if not path:
            return base_url
        return f"{base_url}/{path.strip('/')}"

    def get_jwt(self, client: httpx.Client):
        if not self.credentials:
            assert self.jwt
            return self.jwt

        response = client.post("/accounts/login", json=self.credentials.model_dump())
        if not response.is_success:
            raise RuntimeError(
                f"Login failed with status code: {response.status_code}. Please verify your credentials and base url."
            )
        return LoginResponse.model_validate_json(response.content).token
