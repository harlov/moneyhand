from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction


@dataclass
class UnitOfWorkContext:
    session: AsyncSession
    session_transaction: AsyncSessionTransaction
