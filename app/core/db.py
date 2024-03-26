from sqlmodel import SQLModel, Session, create_engine, select
from collections.abc import Generator
from typing import Annotated
from fastapi import Depends

from app.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

def get_db() -> Generator[Session, None, None]:
  with Session(engine) as session:
    yield session

SessionDep = Annotated[Session, Depends(get_db)]

def init_db() -> None:
  SQLModel.metadata.create_all(engine)

if __name__=="__main__": 
  from app.models import User, PatientInfo, UserType
  init_db()
  admin_user = User(username="dongtd", hashed_password="$2b$12$N/uHi0nEBfCSw0tDSsbpjuQBaFbW7vWjFb0fOadhM.TXFSOMaZ3FC", user_type=UserType.normal)
  session = Session(engine)
  session.add(admin_user)
  session.commit()


