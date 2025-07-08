from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.invoice import Invoice
from app.models.client import Client
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def invoices_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get invoices based on user role
    query = db.query(Invoice)
    if not current_user.is_admin:
        query = query.filter(Invoice.user_id == current_user.id)
    
    invoices = query.order_by(Invoice.created_at.desc()).all()
    
    return templates.TemplateResponse(
        "invoices/list.html", 
        {
            "request": request, 
            "user": current_user,
            "invoices": invoices
        }
    )

@router.get("/create", response_class=HTMLResponse)
async def invoice_create(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "invoices/create.html", 
        {"request": request, "user": current_user}
    )
@router.get("/invoices/create", response_class=HTMLResponse)
async def create_invoice(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    clients = db.query(Client).all()  # Adjust Client import as needed
    return templates.TemplateResponse("invoices/create.html", {
        "request": request,
        "user": current_user,
        "clients": clients
    })