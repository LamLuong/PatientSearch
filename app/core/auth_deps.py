from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import enum
from sqlalchemy import Enum, Column

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, Field, Session, select

from typing import Annotated
from jose import JWTError, jwt
from pydantic import ValidationError, BaseModel
from typing import Any

from app.config import settings

class Token(SQLModel):
  access_token: str
  token_type: str = "bearer"


class TokenData(SQLModel):
  username: str | None = None

class UserType(enum.Enum):
  normal = 0
  admin  = 1

class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  username: str
  hashed_password: str
  user_type: UserType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl=f"{settings.API_V1_STR}/login"
)

TokenDep = Annotated[str, Depends(oauth2_scheme)]

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)


def get_user(db, username: str):
  if username in db:  
    user_dict = db[username]
    return User(**user_dict)

def authenticate_user(*, session: Session, username: str, password: str):
  statement = select(User).where(User.username == username)
  user = session.exec(statement).first()

  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(*, session: Session, token: Annotated[str, Depends(oauth2_scheme)]):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
  
  statement = select(User).where(User.username == username)
  user = session.exec(statement).first()

  if user is None:
    raise credentials_exception
  return user

CurrentUser = Annotated[User, Depends(get_current_user)]