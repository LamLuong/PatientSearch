from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any
from datetime import datetime, timedelta, timezone

from app.core.auth_deps import Token, User, CurrentUser, create_access_token, authenticate_user
from app.core.db import engine, SessionDep
from app.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response) -> Token:
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

  response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
  )
  return Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
def logout_for_release_token(current_user: CurrentUser, response: Response):
  if not current_user:
    raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Not authenticated",
          headers={"WWW-Authenticate": "Bearer"},
        )
  
  response.set_cookie(key="access_token", value="", expires=0)
  return "logged out; please turn off the application and start again"

@router.post("/login/test-token", response_model=User)
def test_token(current_user: CurrentUser) -> User:
  """
  Test access token
  """
  return current_user
