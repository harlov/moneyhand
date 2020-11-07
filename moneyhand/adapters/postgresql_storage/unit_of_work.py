from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

import contextvars
from moneyhand.adapters.postgresql_storage.unit_of_work_context import UnitOfWorkContext
from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.adapters.postgresql_storage.repository import (
    CategoryRepository,
    IncomeRepository,
    SpendingPlanRepository,
)
from moneyhand import config
from . import helpers


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
        self.spending_plan = SpendingPlanRepository(self._context)

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
        await helpers.migrate()

    async def rollback(self):
        c: UnitOfWorkContext = self._context.get()
        await c.session_transaction.rollback()

    async def commit(self):
        c: UnitOfWorkContext = self._context.get()
        await c.session_transaction.commit()
