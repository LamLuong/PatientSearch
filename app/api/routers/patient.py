import aiofiles
import os
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, Response, status, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Relationship, SQLModel, select, func
from fastapi.responses import FileResponse
from datetime import datetime,timezone


from app.models import PatientInfo, PatientInfoBase, PatientsList
from app.core.db import engine, SessionDep
from app.core.auth_deps import CurrentUser

router = APIRouter()

@router.get("/get-patient", response_model=PatientInfo)
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

@router.get("/patient-doc", response_model=PatientInfo)
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

@router.get("/get-patients", response_model=PatientsList)
async def read_items(*, session: SessionDep, current_user: CurrentUser,
                     name:  Annotated[str | None, Query(max_length=100)] = None, seen : bool = None,
                     limit: Annotated[int, Query(ge=1, le=100)] = 2, offset: Annotated[int , Query(ge=1)] = 1):
  if not current_user:
    raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Not authenticated",
          headers={"WWW-Authenticate": "Bearer"},
        )
  count_statement = select(func.count(PatientInfo.document_id))

  if name:
    count_statement = count_statement.where(PatientInfo.name.contains(name))
  if seen is not None:
    count_statement = count_statement.where(PatientInfo.is_downloaded == seen)

  total_record = session.exec(count_statement).one()
  
  if total_record == 0:
    return PatientsList(patients=[], total=0)
  
  statement = select(PatientInfo)

  if name:
    statement = statement.where(PatientInfo.name.contains(name))

  if seen is not None:
    statement = statement.where(PatientInfo.is_downloaded == seen)


  statement = statement.order_by(PatientInfo.created_at).offset((offset - 1)* limit).limit(limit)
  items = session.exec(statement)
  patients_list = PatientsList(patients=items, total=total_record)
  return patients_list


@router.post("/create-patient")
async def create_patient( *, session: SessionDep, current_user: CurrentUser,
                         document_id: str = Form(...),
                         name: str = Form(...),
                         mother_name: str = Form(...),
                         phone: str = Form(...),
                         file: UploadFile) -> Any:
  
  if not current_user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
      )

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
  
  item_db = PatientInfo.model_validate(item, update={"document_path": file.filename, "created_at":datetime.now(timezone.utc)})
  print(item_db.created_at)
  session.add(item_db)
  session.commit()
  session.refresh(item_db)

  return {"status":"update patient 's document sucessfully."}
