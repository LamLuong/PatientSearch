from fastapi import APIRouter

from app.api.routers import health_check, login, view, patient

api_router = APIRouter()
api_router.include_router(health_check.router, tags=["Health"])
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(view.router, tags=["View"])
api_router.include_router(patient.router, tags=["Patient handler"])