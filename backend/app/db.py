import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Use SQLite for local development if PostgreSQL is not available
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./byteforge.db")

# Handle PostgreSQL URL formats if provided
# Handle PostgreSQL URL formats if provided
if DATABASE_URL.startswith("postgres"):
    if DATABASE_URL.startswith("postgresql+psycopg2"):
        DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

# SQLite requires special connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_async_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session