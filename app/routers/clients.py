from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.client import Client
from ..dependencies import get_current_user

router = APIRouter(prefix="/clients")
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def clients_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clients = db.query(Client).filter(Client.is_active == True).all()
    
    return templates.TemplateResponse(
        "clients/list.html", 
        {
            "request": request, 
            "user": current_user,
            "clients": clients
        }
    )

@router.get("/create", response_class=HTMLResponse)
async def client_create(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "clients/create.html", 
        {"request": request, "user": current_user}
    )
