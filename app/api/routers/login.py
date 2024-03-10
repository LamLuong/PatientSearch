from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, Relationship, SQLModel
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any

router = APIRouter()

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login/access-token")
def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
  
  return Token(access_token="hihihihi")