import alembic
from alembic.config import Config as AlembicConfig

from moneyhand import config


async def migrate():
    import asyncio
    from multiprocessing import Process

    p = Process(target=lambda: asyncio.run(_migrate()))
    p.start()
    p.join()


async def _migrate():
    adapters_dir = config.BASE_DIR / "adapters" / "postgresql_storage"

    alembic_ini_path = str(adapters_dir / "alembic.ini")
    migrations_path = str(adapters_dir / "migrations")

    alembic_config = AlembicConfig(alembic_ini_path)
    alembic_config.set_main_option(
        "sqlalchemy.url", f"postgresql://{config.STORAGE_URI}"
    )
    alembic_config.set_main_option("script_location", migrations_path)
    alembic.command.upgrade(alembic_config, "head")
