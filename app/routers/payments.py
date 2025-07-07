from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.payment import Payment

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def payments_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all payments"""
    payments = db.query(Payment).all()
    
    return templates.TemplateResponse("payments/list.html", {
        "request": request,
        "user": current_user,
        "payments": payments,
        "title": "Payments"
    })

@router.get("/create", response_class=HTMLResponse)
async def create_payment(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create payment form"""
    return templates.TemplateResponse("payments/create.html", {
        "request": request,
        "user": current_user,
        "title": "Enter Payment"
    })

@router.post("/create")
async def create_payment_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle payment creation"""
    # TODO: Implement payment creation logic
    return RedirectResponse(url="/payments", status_code=302)

@router.get("/{payment_id}", response_class=HTMLResponse)
async def view_payment(
    payment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific payment"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return templates.TemplateResponse("payments/view.html", {
        "request": request,
        "user": current_user,
        "payment": payment,
        "title": f"Payment #{payment_id}"
    })
