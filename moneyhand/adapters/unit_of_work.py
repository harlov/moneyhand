from dataclasses import dataclass

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncTransaction

import contextvars

from moneyhand.adapters import orm
from moneyhand.adapters.sql_tables import metadata
from moneyhand.adapters.unit_of_work_context import UnitOfWorkContext
from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.adapters.repository import CategoryRepository
from moneyhand import config


class UnitOfWork(AbstractUnitOfWork):
    __slots__ = ["_session"]

    _context: contextvars.ContextVar
    _engine: AsyncEngine

    def __init__(self):
        self._engine = create_async_engine(
            config.STORAGE_URI, echo=config.DEBUG_SQL,
        )
        self._context = contextvars.ContextVar("_context")
        self.category = CategoryRepository(self._context)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        c: UnitOfWorkContext = self._context.get()
        await c.session.__aexit__(exc_type, exc_val, exc_tb)

        self._context.set(None)

    async def __aenter__(self):
        await super().__aenter__()
        session = await (AsyncSession(self._engine).__aenter__())
        session_transaction = await session.begin().__aenter__()
        c = UnitOfWorkContext(
            session=session,
            session_transaction=session_transaction
        )
        self._context.set(c)

    async def setup(self):
        async with self._engine.begin() as t:
            await t.run_sync(orm.Base.metadata.drop_all)
            await t.run_sync(orm.Base.metadata.create_all)

    async def rollback(self):
        c: UnitOfWorkContext = self._context.get()
        await c.session_transaction.rollback()

    async def commit(self):
        c: UnitOfWorkContext = self._context.get()
        await self.category._persist()
        await c.session_transaction.commit()
