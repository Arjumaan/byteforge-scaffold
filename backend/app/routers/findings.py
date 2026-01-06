from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas import FindingCreate
from app import models
from app.deps import get_db, get_current_user

router = APIRouter()

@router.get("/")
async def list_findings(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.exec(select(models.Finding))
    return res.all()

@router.post("/")
async def create_finding(body: FindingCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    finding = models.Finding(**body.dict())
    db.add(finding)
    await db.commit()
    await db.refresh(finding)
    return finding