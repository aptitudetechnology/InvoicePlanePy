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
async def settings_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show settings page"""
    return templates.TemplateResponse("settings/index.html", {
        "request": request,
        "user": current_user,
        "title": "Settings"
    })

@router.get("/company", response_class=HTMLResponse)
async def company_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show company settings"""
    return templates.TemplateResponse("settings/company.html", {
        "request": request,
        "user": current_user,
        "title": "Company Settings"
    })

@router.get("/users", response_class=HTMLResponse)
async def user_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show user management"""
    users = db.query(User).all()
    return templates.TemplateResponse("settings/users.html", {
        "request": request,
        "user": current_user,
        "users": users,
        "title": "User Management"
    })

@router.get("/invoice", response_class=HTMLResponse)
async def invoice_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice settings"""
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Settings"
    })
