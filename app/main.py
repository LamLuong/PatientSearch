from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import settings


def custom_generate_unique_id(route: APIRoute):
  return f"{route.tags[0]}-{route.name}"


app = FastAPI(
  title=settings.PROJECT_NAME,
  openapi_url=f"/openapi.json",
  generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
  app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
