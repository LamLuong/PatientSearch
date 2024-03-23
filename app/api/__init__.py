from fastapi import APIRouter

from app.api.routers import health_check, login, view, patient
from app.config import settings

api_router = APIRouter()
api_router.include_router(health_check.router, tags=["Health"])
api_router.include_router(login.router, prefix=settings.API_V1_STR, tags=["Login"])
api_router.include_router(view.router, tags=["View"])
api_router.include_router(patient.router, tags=["Patient handler"])