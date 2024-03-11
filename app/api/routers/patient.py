from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, Relationship, SQLModel
from fastapi.responses import FileResponse

router = APIRouter()

class Patient(SQLModel):
  id: str
  name: str
  mother_name: str
  phone : str


@router.get("/patient-info", response_model=Patient)
def read_patient(patient_id: str) -> Any:
  print("patient_id", patient_id)
  if not patient_id:
    raise HTTPException(status_code=404, detail="Patient id is empty!")
  
  return Patient(id="dsa", name="Tran Minh Anh", mother_name="Nguyen Minh Trang", phone="0345689963")

@router.get("/patient-result")
async def main():
    return FileResponse("/home/lamlt/Downloads/2110.06864.pdf")
