from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app import models
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET = settings.JWT_SECRET
ALG = settings.JWT_ALGORITHM

async def get_db() -> AsyncSession:
    async for s in get_session():
        yield s

from sqlmodel import select

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> models.User:
    creds_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALG])
        email: str = payload.get("sub")
        if email is None:
            raise creds_exc
    except JWTError:
        raise creds_exc
    
    res = await db.exec(select(models.User).where(models.User.email == email))
    user = res.first()
    if not user:
        raise creds_exc
    return user