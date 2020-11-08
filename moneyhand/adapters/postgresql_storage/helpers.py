from typing import Tuple, Any, Dict
from multiprocessing import Process

import alembic
from alembic.config import Config as AlembicConfig
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.functions import GenericFunction, Function
from sqlalchemy.dialects import postgresql as pg
import sqlalchemy as sa

from moneyhand import config


def migrate(only_structure: bool = False):
    p = Process(target=_migrate, kwargs={"only_structure": only_structure})
    p.start()
    p.join()


def _migrate(only_structure: bool = False):
    adapters_dir = config.BASE_DIR / "adapters" / "postgresql_storage"

    alembic_ini_path = str(adapters_dir / "alembic.ini")
    migrations_path = str(adapters_dir / "migrations")

    alembic_config = AlembicConfig(alembic_ini_path)
    alembic_config.set_main_option(
        "sqlalchemy.url", f"postgresql://{config.STORAGE_URI}"
    )
    if only_structure:
        alembic_config.set_main_option("only_structure", "1")

    alembic_config.set_main_option("script_location", migrations_path)
    alembic.command.upgrade(alembic_config, "head")


class JSONBAggFunction(GenericFunction):
    name = "jsonb_agg"
    type = pg.JSONB


def jsonb_agg(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> JSONBAggFunction:
    return JSONBAggFunction(*args, **kwargs)


def json_build_object(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Function:
    return sa.func.json_build_object(*args, **kwargs)


def s(value: str) -> TextClause:
    return sa.text("'{0}'".format(value))
