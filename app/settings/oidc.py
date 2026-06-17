from pydantic import BaseModel


class OIDCConfig(BaseModel):
    username: str = "admin"
    password: str = "admin"
    client_id: str = "client"
    realm: str = "realm"
    base_url: str = "http://localhost"
