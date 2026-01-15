from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas import TargetCreate
from app import models
from app.deps import get_db, get_current_user
from app.audit import log_security_event

router = APIRouter()

@router.get("/")
async def list_targets(db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    res = await db.exec(select(models.Target))
    targets = res.all()
    for t in targets:
        t.decrypt_fields()
    return targets

@router.post("/")
async def create_target(body: TargetCreate, db: AsyncSession = Depends(get_db), user: models.User = Depends(get_current_user)):
    target = models.Target(**body.dict())
    target.encrypt_fields()
    db.add(target)
    await db.commit()
    await db.refresh(target)
    
    log_security_event("TARGET_CREATED", user.email, {"target_id": target.id, "name": body.name})
    
    target.decrypt_fields()
    return target