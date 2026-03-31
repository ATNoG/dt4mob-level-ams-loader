import asyncio

import pydantic_argparse

from app.hono_connection import Hono
from app.level_ams_loader import LevelAMSLoader
from app.settings import settings
from app.settings.loader_constraints import LoaderConstraints


def main() -> None:
    parser = pydantic_argparse.ArgumentParser(
        model=LoaderConstraints,
        prog="LevelAMS API Ditto Loader",
        add_help=True,
        exit_on_error=True,
    )
    args = parser.parse_typed_args()

    hono = Hono(settings.hono)
    loader = LevelAMSLoader(hono, settings.loader, args)

    asyncio.run(loader.run())


if __name__ == "__main__":
    main()
