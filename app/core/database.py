from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncIterator
from fastapi import Depends
from typing import Annotated
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine (
  settings.database_url,
  pool_pre_ping=True,
  echo=True,
)

AsyncSessionLocal = async_sessionmaker (
  bind=engine,
  class_=AsyncSession,
  autoflush=False,
  expire_on_commit=False
)

class Base(DeclarativeBase):
  pass

async def getSession() -> AsyncIterator[AsyncSession]:
  async with AsyncSessionLocal() as session:
    try:
      yield session
    except Exception:
      await session.rollback()
      raise

DBSession = Annotated[AsyncSession, Depends(getSession)]
