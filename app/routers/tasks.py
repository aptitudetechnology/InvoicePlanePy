from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.task import Task, Project, TaskStatus, TaskPriority
from app.models.client import Client

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Tasks routes
@router.get("/", response_class=HTMLResponse)
async def tasks_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all tasks"""
    query = db.query(Task)
    if not current_user.role == 'admin':
        query = query.filter(
            (Task.user_id == current_user.id) | 
            (Task.assigned_to_id == current_user.id)
        )
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
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
    projects = db.query(Project).filter(Project.is_active == True).all()
    clients = db.query(Client).filter(Client.is_active == True).all()
    users = db.query(User).all()
    
    return templates.TemplateResponse("tasks/create.html", {
        "request": request,
        "user": current_user,
        "projects": projects,
        "clients": clients,
        "users": users,
        "task_statuses": TaskStatus,
        "task_priorities": TaskPriority,
        "title": "Create Task"
    })

@router.post("/create")
async def create_task_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    status: str = Form(TaskStatus.NOT_STARTED.value),
    priority: str = Form(TaskPriority.NORMAL.value),
    project_id: Optional[int] = Form(None),
    client_id: Optional[int] = Form(None),
    assigned_to_id: Optional[int] = Form(None),
    start_date: Optional[str] = Form(None),
    due_date: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle task creation"""
    task = Task(
        name=name,
        description=description,
        status=TaskStatus(status),
        priority=TaskPriority(priority),
        project_id=project_id if project_id else None,
        client_id=client_id if client_id else None,
        assigned_to_id=assigned_to_id if assigned_to_id else None,
        user_id=current_user.id,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        due_date=datetime.fromisoformat(due_date) if due_date else None
    )
    
    db.add(task)
    db.commit()
    
    return RedirectResponse(url="/tasks", status_code=302)

@router.get("/{task_id}", response_class=HTMLResponse)
async def view_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if not current_user.role == 'admin' and task.user_id != current_user.id and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return templates.TemplateResponse("tasks/view.html", {
        "request": request,
        "user": current_user,
        "task": task,
        "title": f"Task: {task.name}"
    })

# Projects routes
@router.get("/projects", response_class=HTMLResponse)
async def projects_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all projects"""
    query = db.query(Project)
    if not current_user.role == 'admin':
        query = query.filter(Project.user_id == current_user.id)
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    return templates.TemplateResponse("tasks/projects.html", {
        "request": request,
        "user": current_user,
        "projects": projects,
        "title": "Projects"
    })

@router.get("/projects/create", response_class=HTMLResponse)
async def create_project(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create project form"""
    clients = db.query(Client).filter(Client.is_active == True).all()
    
    return templates.TemplateResponse("tasks/create_project.html", {
        "request": request,
        "user": current_user,
        "clients": clients,
        "title": "Create Project"
    })

@router.post("/projects/create")
async def create_project_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    client_id: Optional[int] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle project creation"""
    project = Project(
        name=name,
        description=description,
        client_id=client_id if client_id else None,
        user_id=current_user.id,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        end_date=datetime.fromisoformat(end_date) if end_date else None
    )
    
    db.add(project)
    db.commit()
    
    return RedirectResponse(url="/tasks/projects", status_code=302)

@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def view_project(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check permissions
    if not current_user.role == 'admin' and project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get tasks for this project
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    
    return templates.TemplateResponse("tasks/view_project.html", {
        "request": request,
        "user": current_user,
        "project": project,
        "tasks": tasks,
        "title": f"Project: {project.name}"
    })
    # TODO: Implement task fetching
    return templates.TemplateResponse("tasks/view.html", {
        "request": request,
        "user": current_user,
        "task_id": task_id,
        "title": f"Task #{task_id}"
    })
