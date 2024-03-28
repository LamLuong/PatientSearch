import aiofiles
import os
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, Response, status
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Relationship, SQLModel
from fastapi.responses import FileResponse


from app.models import PatientInfo, PatientInfoBase
from app.core.db import engine, SessionDep
from app.core.auth_deps import CurrentUser
from sqlmodel import select

router = APIRouter()

@router.get("/get-patient/", response_model=PatientInfo)
async def read_item(*, session: SessionDep, document_id: str):
  if not document_id:
    raise HTTPException(
            status_code=422,
            detail="Invalid input",
            headers={"X-Error": "There goes my error"},
    ) 
  
  item = session.get(PatientInfo, document_id)
  if not item:
    raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
    )
  return item

@router.get("/patient-doc/", response_model=PatientInfo)
async def patient_doc(*, document_name: str, response: Response):
  file_name = "./files/" + document_name
  print(file_name)
  if not os.path.isfile(file_name):
    raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
    )        
  f = open(file_name, "rb")
  headers = {"Content-Disposition": "inline; filename=" + document_name}
  response = StreamingResponse(f, media_type="application/pdf", headers=headers)
  return response

@router.get("/get-patients/", response_model=List[PatientInfo])
async def read_items(*, session: SessionDep, current_user: CurrentUser, limit: int = 5, offset: int = 0):
  if not current_user:
    raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Not authenticated",
          headers={"WWW-Authenticate": "Bearer"},
        )
  statement = select(PatientInfo).offset(offset).limit(limit)
  items = session.exec(statement)

  return items


@router.post("/create-patient")
async def create_patient( *, session: SessionDep, current_user: CurrentUser,
                         document_id: str = Form(...),
                         name: str = Form(...),
                         mother_name: str = Form(...),
                         phone: str = Form(...),
                         file: UploadFile) -> Any:
  
  if file.content_type != "application/pdf":
    raise HTTPException(400, detail="Invalid pdf document type")
  
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
