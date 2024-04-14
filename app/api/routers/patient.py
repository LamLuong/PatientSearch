import aiofiles
import os
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, Response, status, Query, Path
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Relationship, SQLModel, select, func
from fastapi.responses import FileResponse
from datetime import datetime,timezone


from app.models import PatientInfo, PatientInfoBase, PatientsList
from app.core.db import engine, SessionDep
from app.core.auth_deps import CurrentUser, credentials_exception

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
  item.is_downloaded = True
  session.add(item)
  session.commit()
  session.refresh(item)
  return item

@router.get("/patient-doc", response_model=PatientInfo)
async def patient_doc(*, document_name: str, response: Response):
  file_name = "./files/" + document_name

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
                     specialist: Annotated[int, Query(ge=0, le=3)] = 0,
                     limit: Annotated[int, Query(ge=1, le=100)] = 100, offset: Annotated[int , Query(ge=1)] = 1):
  if not current_user:
    raise credentials_exception
  
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

  if specialist > 0:
    statement = statement.where(PatientInfo.specialist == specialist)


  statement = statement.order_by(PatientInfo.created_at.desc()).offset((offset - 1)* limit).limit(limit)
  items = session.exec(statement)
  patients_list = PatientsList(patients=items, total=total_record)
  return patients_list


@router.post("/create-patient")
async def create_patient( *, session: SessionDep, current_user: CurrentUser,
                         document_id: str = Form(...),
                         name: str = Form(min_length=1, max_length=50),
                         mother_name: str = Form(min_length=1, max_length=50),
                         phone: str = Form(min_length=10, max_length=13),
                         specialist: int = Form(gt=0, lt=4),
                         file: UploadFile) -> Any:
  
  if not current_user:
    raise credentials_exception

  if file.content_type != "application/pdf":
    raise HTTPException(400, detail="Invalid pdf document type")
  
  out_file_path = "./files/" + document_id + ".pdf"
  async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
  try:
    item = PatientInfoBase(document_id=document_id,
                     name=name,
                     mother_name=mother_name,
                     phone=phone,
                     specialist=specialist)
  except:
    raise HTTPException(status_code=422, detail="Invalid input")
  
  item_db = PatientInfo.model_validate(item, update={"created_at":datetime.now(timezone.utc)})
  
  try:
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
  except:
    raise HTTPException(status_code=422, detail="Canot not duplicate document id")
  
  return {"status":"update patient 's document sucessfully."}

@router.delete("/delete-patient/{document_id}")
async def create_patient( *, session: SessionDep, current_user: CurrentUser,
                         document_id:  Annotated[str, Path(min_length=1, max_length=100)]):
  
  if not current_user:
    raise credentials_exception
  
  patient = session.get(PatientInfo, document_id)
  if not patient:
    raise HTTPException(status_code=404, detail="Patient not found")
  session.delete(patient)
  session.commit()
  os.remove("./files/" + document_id + ".pdf")

  return {"status":"delete patient 's document sucessfully."}

