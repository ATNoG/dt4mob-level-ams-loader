import sys
from typing import Literal, Self

from loguru import logger
from pydantic import model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from app.settings.ditto import DittoConfig
from app.settings.history_loading import HistoryLoadingConfig
from app.settings.hono import HonoConfig
from app.settings.loader import LoaderConfig

type LogLevel = Literal[
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="config.toml",
        env_prefix="LEVEL_AMS_LOADER_",
        env_nested_delimiter="__",
    )

    log_level: LogLevel = "INFO"

    history: HistoryLoadingConfig = HistoryLoadingConfig()

    loader: LoaderConfig = LoaderConfig()
    hono: HonoConfig

    ditto: DittoConfig = DittoConfig()

    @model_validator(mode="after")
    def validate_credentials(self) -> Self:
        if not self.loader.jwt and not self.loader.credentials:
            raise ValueError("Provide at least one of jwt or credentials")
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            TomlConfigSettingsSource(settings_cls),
        )


settings = Settings()

logger.remove()
logger.add(sys.stdout, level=settings.log_level)

logger.debug(settings)
