from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session
from typing import Generator

async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session

    finally:
        await session.close()
