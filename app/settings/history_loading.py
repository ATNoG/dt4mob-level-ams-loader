from typing import Optional

from pydantic import AnyHttpUrl, BaseModel


class HistoryLoadingConfig(BaseModel):
    enabled: bool = False

    base_url: AnyHttpUrl = AnyHttpUrl("http://127.0.0.1/historic")

    username: Optional[str] = None
    password: Optional[str] = None
