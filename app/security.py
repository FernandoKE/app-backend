from datetime import datetime, timedelta
from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session

from app import crud
from app.config import settings
from app.database import get_session
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, session: Session) -> User:
    try:
        user = crud.select_user_by_username(username, session)
        if not verify_password(password, user.password):
            raise Exception("Incorrect password")
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    return user


def create_jwt(data: dict, expires_delta: timedelta = timedelta(days=1)) -> str:
    to_encode = {
        **data,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + expires_delta,
    }
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    credentials_exception = auth_exception(detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.select_user_by_username(username, session)

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def auth_exception(detail: str = "Invalid authentication"):
    return HTTPException(status_code=401, detail=detail)


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        user_roles = [g.name for g in user.roles]
        for role in self.allowed_roles:
            if role in user_roles:
                return
        raise HTTPException(status_code=403, detail="Operation not permited")
