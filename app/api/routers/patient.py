import aiofiles
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from sqlmodel import Field, Relationship, SQLModel
from fastapi.responses import FileResponse

from app.models import PatientInfo, PatientInfoBase
from app.core.db import engine, SessionDep
from app.core.auth_deps import CurrentUser
router = APIRouter()

@router.get("/get-patient/", response_model=PatientInfo)
async def read_items(*, session: SessionDep, document_id: str):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    item = session.get(PatientInfo, document_id)

    return item

@router.post("/create-patient")
async def create_patient( *, session: SessionDep, current_user: CurrentUser,
                         document_id: str = Form(...),
                         name: str = Form(...),
                         mother_name: str = Form(...),
                         phone: str = Form(...),
                         file: UploadFile) -> Any:
  
  out_file_path = "./files/" + file.filename
  async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
  try:
    item = PatientInfoBase(document_id=document_id,
                     name=name,
                     mother_name=mother_name,
                     phone=phone)
  except:
    raise HTTPException(status_code=422, detail="Invalid input")
  
  item_db = PatientInfo.model_validate(item, update={"document_path": file.filename})
  session.add(item_db)
  session.commit()
  session.refresh(item_db)

  return {"status":"update patient 's document sucessfully."}
