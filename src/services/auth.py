from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.db.db import get_db
from src.conf.config import config
from src.services.users import UserService


class Hash:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def get_pwd_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)


# OAuth2 configuration for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        timedelta(seconds=expires_delta)
        if expires_delta
        else timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGO)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    if not user:
        raise credentials_exception
    return user


def create_email_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=config.MAIL_TOKEN_EXP_DAYS)
    to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGO)


async def get_email_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
        email = payload.get("sub")
        if not email:
            raise ValueError("Email not found in token payload")
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email verification token",
        )