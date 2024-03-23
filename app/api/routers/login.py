from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any
from datetime import datetime, timedelta, timezone

from app.core.auth_deps import Token, User, create_access_token, authenticate_user
from app.core.db import engine, SessionDep
from app.config import settings

router = APIRouter()

@router.post("/login/")
def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
  user = authenticate_user(session=session, username=form_data.username, password=form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
        )

  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
      data={"sub": user.username}, expires_delta=access_token_expires
  )
  return Token(access_token=access_token, token_type="bearer")

