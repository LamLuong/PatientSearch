from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select

from typing import Annotated
from jose import JWTError, jwt
from pydantic import ValidationError, BaseModel
from typing import Any

from app.core.db import SessionDep
from app.config import settings
from app.core.utils import OAuth2PasswordBearerWithCookie
from app.models import Token, UserType, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(
#   tokenUrl=f"{settings.API_V1_STR}/login"
# )
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl=f"{settings.API_V1_STR}/login", auto_error=False)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)


def get_user(db, username: str):
  if username in db:  
    user_dict = db[username]
    return User(**user_dict)

def authenticate_user(*, session: SessionDep, username: str, password: str):
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

TokenDep = Annotated[str, Depends(oauth2_scheme)]
async def get_current_user(*, session: SessionDep, token: TokenDep):
  if not token:
    return None
  
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      return None
  except JWTError:
    return None
  
  statement = select(User).where(User.username == username)
  user = session.exec(statement).first()

  return user

CurrentUser = Annotated[User, Depends(get_current_user)]