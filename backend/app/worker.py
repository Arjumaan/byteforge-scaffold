import os
from celery import Celery
from app.tasks import run_job

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

def enqueue_job(job_id: int, kind: str):
    celery_app.send_task("app.tasks.run_job", args=[job_id, kind])