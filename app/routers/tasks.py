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
async def tasks_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all tasks"""
    # TODO: Implement Task model and fetch tasks
    tasks = []  # Placeholder
    
    return templates.TemplateResponse("tasks/list.html", {
        "request": request,
        "user": current_user,
        "tasks": tasks,
        "title": "Tasks"
    })

@router.get("/create", response_class=HTMLResponse)
async def create_task(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create task form"""
    return templates.TemplateResponse("tasks/create.html", {
        "request": request,
        "user": current_user,
        "title": "Create Task"
    })

@router.get("/{task_id}", response_class=HTMLResponse)
async def view_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific task"""
    # TODO: Implement task fetching
    return templates.TemplateResponse("tasks/view.html", {
        "request": request,
        "user": current_user,
        "task_id": task_id,
        "title": f"Task #{task_id}"
    })
