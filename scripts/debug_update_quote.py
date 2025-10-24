from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def quotes_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display quotes list page"""
    return templates.TemplateResponse(
        "quotes/list.html",
        {
            "request": request,
            "user": current_user,
            "title": "Quotes"
        }
    )

@router.get("/create", response_class=HTMLResponse)
async def create_quote_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display create quote form"""
    return templates.TemplateResponse(
        "quotes/create.html",
        {
            "request": request,
            "user": current_user,
            "title": "Create Quote"
        }
    )

@router.post("/create")
async def create_quote(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new quote"""
    # TODO: Implement quote creation logic
    # For now, just return success
    return {"message": "Quote created successfully"}

@router.get("/{quote_id}", response_class=HTMLResponse)
async def view_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific quote"""
    # TODO: Implement quote retrieval logic
    return templates.TemplateResponse(
        "quotes/view.html",
        {
            "request": request,
            "user": current_user,
            "quote_id": quote_id,
            "title": f"Quote #{quote_id}"
        }
    )

@router.get("/{quote_id}/edit", response_class=HTMLResponse)
async def edit_quote_form(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display edit quote form"""
    # TODO: Implement quote retrieval logic
    return templates.TemplateResponse(
        "quotes/edit.html",
        {
            "request": request,
            "user": current_user,
            "quote_id": quote_id,
            "title": f"Edit Quote #{quote_id}"
        }
    )

@router.post("/{quote_id}/edit")
async def edit_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a quote"""
    # TODO: Implement quote update logic
    return {"message": f"Quote {quote_id} updated successfully"}

@router.delete("/{quote_id}")
async def delete_quote(
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a quote"""
    # TODO: Implement quote deletion logic
    return {"message": f"Quote {quote_id} deleted successfully"}

# API endpoints for AJAX requests
@router.get("/api/quotes", response_model=List[dict])
async def get_quotes_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get quotes via API"""
    # TODO: Implement quote retrieval logic
    return [
        {
            "id": 1,
            "quote_number": "Q-2024-001",
            "client_name": "Sample Client",
            "date_created": datetime.now().isoformat(),
            "total": 1000.00,
            "status": "draft"
        }
    ]

@router.post("/api/quotes")
async def create_quote_api(
    quote_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create quote via API"""
    # TODO: Implement quote creation logic
    return {"message": "Quote created successfully", "quote_id": 1}