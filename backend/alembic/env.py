import os
import sys
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from sqlmodel import SQLModel

# Ensure /app is on sys.path when Alembic runs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

config = context.config

# Safe logging setup
if config.config_file_name and os.path.isfile(config.config_file_name):
    try:
        fileConfig(config.config_file_name, disable_existing_loggers=False)
    except KeyError:
        pass

from app import models  # noqa: E402,F401

target_metadata = SQLModel.metadata
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appuser:appsecret@db:5432/pentest")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, future=True)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())