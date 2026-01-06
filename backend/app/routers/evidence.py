from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas import EvidenceCreate
from app import models
from app.deps import get_db, get_current_user

router = APIRouter()

@router.get("/")
async def list_evidence(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.exec(select(models.Evidence))
    return res.all()

@router.post("/")
async def create_evidence(body: EvidenceCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    ev = models.Evidence(**body.dict())
    db.add(ev)
    await db.commit()
    await db.refresh(ev)
    return ev