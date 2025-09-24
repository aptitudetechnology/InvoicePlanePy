from fastapi import APIRouter, Depends, Request, HTTPException
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


@router.get("/{invoice_id}", response_class=HTMLResponse)
async def view_invoice(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """View a specific invoice"""
    from sqlalchemy.orm import joinedload
    invoice = db.query(Invoice).options(
        joinedload(Invoice.client),
        joinedload(Invoice.items)
    ).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Check permissions
    if not current_user.is_admin and invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return templates.TemplateResponse(
        "invoices/view.html",
        {
            "request": request,
            "user": current_user,
            "invoice": invoice,
            "title": f"Invoice #{invoice.invoice_number}",
        },
    )
"""
@router.get("/create", response_class=HTMLResponse)
async def invoice_create(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "invoices/create.html", 
        {"request": request, "user": current_user}
    )
"""    

@router.get("/create", response_class=HTMLResponse)
async def create_invoice(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    clients = db.query(Client).all()
    return templates.TemplateResponse("invoices/create.html", {
        "request": request,
        "user": current_user,
        "clients": clients
    })

# POST /invoices/ - handle invoice details form submission
from fastapi import Form

@router.post("/", response_class=HTMLResponse)
async def invoice_create_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    client_id: int = Form(...),
    invoice_number: str = Form(None),
    status: str = Form(None),
    invoice_date: str = Form(None),
    due_date: str = Form(None),
    payment_method: str = Form(None),
    pdf_password: str = Form(None),
    invoice_terms: str = Form(None)
    # Add other fields as needed
):
    client = db.query(Client).filter(Client.id == client_id).first()
    # Here you would process and save the invoice, for now just show a confirmation
    return templates.TemplateResponse("invoices/details.html", {
        "request": request,
        "user": current_user,
        "client": client,
        "message": "Invoice POST received"
    })

    