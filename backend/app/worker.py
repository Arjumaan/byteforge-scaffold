import os
import threading
# from celery import Celery
from app.tasks import run_job

# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

def enqueue_job(job_id: int, kind: str):
    """
    Enqueue a job for background processing.
    For local development, we skip Redis/Celery and use a background thread.
    """
    print(f"[*] Starting job {job_id} ({kind}) in background thread...")
    thread = threading.Thread(target=run_job, args=(job_id, kind))
    thread.daemon = True
    thread.start()