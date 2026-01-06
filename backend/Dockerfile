FROM python:3.11-slim
WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=false PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry && poetry install --no-interaction --no-ansi
COPY . .
EXPOSE 8000