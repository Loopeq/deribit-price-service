from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import db_session


async def get_db() -> AsyncIterator[AsyncSession]:
    async with db_session() as session:
        yield session
