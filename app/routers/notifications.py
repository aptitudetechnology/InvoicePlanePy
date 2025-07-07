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
async def notifications_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show notifications page"""
    # TODO: Implement notification system
    notifications = []  # Placeholder
    
    return templates.TemplateResponse("notifications/index.html", {
        "request": request,
        "user": current_user,
        "notifications": notifications,
        "title": "Notifications"
    })
