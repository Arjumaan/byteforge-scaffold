from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas import TargetCreate
from app import models
from app.deps import get_db, get_current_user

router = APIRouter()

@router.get("/")
async def list_targets(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.exec(select(models.Target))
    return res.all()

@router.post("/")
async def create_target(body: TargetCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    target = models.Target(**body.dict())
    db.add(target)
    await db.commit()
    await db.refresh(target)
    return target