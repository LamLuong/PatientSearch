from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.get("/health-check")
async def health_check():
    return {"message": "OK"}

