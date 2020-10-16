import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

import contextvars
import alembic
from alembic.config import Config as AlembicConfig


from moneyhand.adapters import orm
from moneyhand.adapters.unit_of_work_context import UnitOfWorkContext
from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.adapters.repository import CategoryRepository, IncomeRepository
from moneyhand import config


class UnitOfWork(AbstractUnitOfWork):
    __slots__ = ["_session"]

    _context: contextvars.ContextVar
    _engine: AsyncEngine

    def __init__(self):
        self._engine = create_async_engine(
            f"postgresql+asyncpg://{config.STORAGE_URI}",
            echo=config.DEBUG_SQL,
        )
        self._context = contextvars.ContextVar("_context")
        self.category = CategoryRepository(self._context)
        self.income = IncomeRepository(self._context)

    async def __aenter__(self):
        await super().__aenter__()
        session = await (AsyncSession(self._engine).__aenter__())
        session_transaction = await session.begin()
        c = UnitOfWorkContext(session=session, session_transaction=session_transaction)
        self._context.set(c)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        c: UnitOfWorkContext = self._context.get()
        await c.session.__aexit__(exc_type, exc_val, exc_tb)

        self._context.set(None)

    async def setup(self):
        adapters_dir = config.BASE_DIR / "adapters"

        alembic_ini_path = str(adapters_dir / "alembic.ini")
        migrations_path = str(adapters_dir / "migrations")

        alembic_config = AlembicConfig(alembic_ini_path)
        alembic_config.set_main_option(
            "sqlalchemy.url", f"postgresql://{config.STORAGE_URI}"
        )
        alembic_config.set_main_option("script_location", migrations_path)
        alembic.command.upgrade(alembic_config, "head")

    async def rollback(self):
        c: UnitOfWorkContext = self._context.get()
        await c.session_transaction.rollback()

    async def commit(self):
        c: UnitOfWorkContext = self._context.get()
        await c.session_transaction.commit()
