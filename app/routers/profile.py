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
async def profile_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show user profile page"""
    return templates.TemplateResponse("profile/index.html", {
        "request": request,
        "user": current_user,
        "title": "User Profile"
    })

@router.get("/edit", response_class=HTMLResponse)
async def edit_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show edit profile form"""
    return templates.TemplateResponse("profile/edit.html", {
        "request": request,
        "user": current_user,
        "title": "Edit Profile"
    })
