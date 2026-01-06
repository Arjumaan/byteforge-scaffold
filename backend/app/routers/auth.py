from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas import UserCreate, Token, UserOut
from app import models
from app.deps import get_db
from app.auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    res = await db.exec(select(models.User).where(models.User.email == user_in.email))
    if res.first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Simple logic for first user being admin, otherwise user
    count_res = await db.exec(select(models.User))
    is_first_user = count_res.first() is None
    role = "admin" if is_first_user else "user"
    
    user = models.User(
        email=user_in.email, 
        hashed_password=hash_password(user_in.password), 
        role=role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut(id=user.id, email=user.email, role=user.role)

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    res = await db.exec(select(models.User).where(models.User.email == form_data.username))
    user = res.first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_token(user.email)
    return Token(access_token=token)