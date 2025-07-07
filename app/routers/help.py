from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def help_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Show help page"""
    return templates.TemplateResponse("help/index.html", {
        "request": request,
        "user": current_user,
        "title": "Help & Documentation"
    })

@router.get("/faq", response_class=HTMLResponse)
async def faq_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Show FAQ page"""
    return templates.TemplateResponse("help/faq.html", {
        "request": request,
        "user": current_user,
        "title": "Frequently Asked Questions"
    })

@router.get("/documentation", response_class=HTMLResponse)
async def documentation_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Show documentation page"""
    return templates.TemplateResponse("help/documentation.html", {
        "request": request,
        "user": current_user,
        "title": "Documentation"
    })
