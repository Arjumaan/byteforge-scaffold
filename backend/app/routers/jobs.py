from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas import JobCreate
from app import models
from app.deps import get_db, get_current_user
from app.worker import enqueue_job

router = APIRouter()

@router.get("/")
async def list_jobs(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.exec(select(models.Job))
    return res.all()

@router.post("/")
async def create_job(body: JobCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    target = await db.get(models.Target, body.target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    job = models.Job(target_id=body.target_id, kind=body.kind, status="queued")
    db.add(job)
    await db.commit()
    await db.refresh(job)
    enqueue_job(job.id, body.kind)
    return job