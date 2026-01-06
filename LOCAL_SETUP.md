# Local Setup Guide (Non-Docker)

If you prefer not to use Docker, follow these steps to set up the ByteForge Scaffold locally.

## 1. Prerequisites
- **Postgres**: Install PostgreSQL 16+. Create a database named `pentest`.
- **Redis**: Install Redis 7+. Ensure it is running on `localhost:6379`.
- **Python**: 3.11+
- **Node.js**: 18+

## 2. Infrastructure Setup (Manual)
1. Start your local **PostgreSQL** server.
2. Create a user `appuser` with password `appsecret` (or update environment variables).
3. Create a database `pentest`.
4. Start your local **Redis** server.

## 3. Backend Setup
1. Open a terminal in `./backend`.
2. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
3. Set environment variables:
   ```bash
   # Windows (PowerShell)
   $env:DATABASE_URL="postgresql+asyncpg://appuser:appsecret@localhost:5432/pentest"
   $env:REDIS_URL="redis://localhost:6379/0"
   $env:JWT_SECRET="arjumaan"
   $env:PYTHONPATH="."
   ```
4. Run migrations:
   ```bash
   poetry run alembic upgrade head
   ```
5. Start the API:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
6. Start the Worker (in a separate terminal):
   ```bash
   $env:DATABASE_URL="postgresql+asyncpg://appuser:appsecret@localhost:5432/pentest"
   $env:REDIS_URL="redis://localhost:6379/0"
   $env:PYTHONPATH="."
   poetry run celery -A app.worker.celery_app worker -l info
   ```

## 4. Frontend Setup
1. Open a terminal in `./frontend`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

## Why Docker? (Just as a reminder)
- **Isolation**: No need to install Postgres/Redis on your actual machine.
- **Consistency**: Guarantees the same versions of libraries and DB for every developer.
- **Simplicity**: One command (`docker compose up`) vs. starting 4-5 different terminals and services manually.
