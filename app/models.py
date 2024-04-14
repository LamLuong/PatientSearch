import enum, re
from sqlmodel import SQLModel, Field, DateTime
from pydantic import validator
from datetime import datetime
from typing import  List

class Token(SQLModel):
  access_token: str
  token_type: str = "bearer"

class UserType(enum.Enum):
  normal = 0
  admin  = 1

class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  username: str
  hashed_password: str
  user_type: UserType

class PatientInfoBase(SQLModel):
  document_id: str | None = Field(default=None, primary_key=True)
  name: str = Field(min_length=1, max_length=50)
  mother_name: str = Field(min_length=1, max_length=50)
  phone: str = Field(min_length=10, max_length=13)
  specialist: int = Field(gt=0, lt=4) # 1: Khoa Sản; 2: khoa Điều trị theo yêu cầu, 3:khoa Sơ Sinh

  @validator("phone")
  def phone_validation(cls, v):
    regex = r"^[0]{1}[1-9]{2}[0-9]{7}$"
    if v and not re.search(regex, v, re.I):
      raise ValueError("Phone Number Invalid.")
    return v

class PatientInfo(PatientInfoBase, table=True):
  __tablename__ = "patient_info"

  # document_path: str
  is_downloaded: bool = Field(default=False)
  created_at:  datetime = Field(DateTime(timezone=True), nullable=False)

class PatientsList(SQLModel):
  patients: List[PatientInfo]
  total: int = 0
