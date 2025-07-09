from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.client import Client  # <-- Add this import
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
@router.get("/", response_class=HTMLResponse)
async def quotes_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all quotes"""
    # TODO: Implement Quote model and fetch quotes
    quotes = []  # Placeholder
    return templates.TemplateResponse("quotes/list.html", {
        "request": request,
        "user": current_user,
        "quotes": quotes,
        "title": "Quotes"
    })
@router.get("/create", response_class=HTMLResponse)
async def create_quote(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create quote form"""
    clients = db.query(Client).all()  # <-- Fetch clients from DB
    return templates.TemplateResponse("quotes/create.html", {
        "request": request,
        "user": current_user,
        "clients": clients,  # <-- Pass clients to template
        "title": "Create Quote"
    })
@router.post("/create")
async def create_quote_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle quote creation"""
    # TODO: Implement quote creation logic
    return RedirectResponse(url="/quotes", status_code=302)
@router.get("/{quote_id}", response_class=HTMLResponse)
async def view_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific quote"""
    # TODO: Implement quote fetching
    return templates.TemplateResponse("quotes/view.html", {
        "request": request,
        "user": current_user,
        "quote_id": quote_id,
        "title": f"Quote #{quote_id}"
    })