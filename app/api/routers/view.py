from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.auth_deps import CurrentUser

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request, current_user: CurrentUser):
  username = None
  if current_user:
    username = current_user.username

  return templates.TemplateResponse(
    request=request, name="index.html", context={"request":request ,"username" : username}
  )

@router.get("/admin", response_class=HTMLResponse)
async def view_item(request: Request, current_user: CurrentUser):

  return templates.TemplateResponse(
    request=request, name="index.html", context={"id": 10}
  )