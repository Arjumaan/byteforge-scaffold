import asyncio
import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appuser:appsecret@db:5432/pentest")
# Allow fallback if someone sets psycopg2 URL by mistake
if DATABASE_URL.startswith("postgresql+psycopg2"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session