from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.client import Client
from app.models.invoice import Invoice
from app.models.payment import Payment

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def reports_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show reports dashboard"""
    
    # Calculate basic statistics
    total_clients = db.query(func.count(Client.id)).scalar()
    total_invoices = db.query(func.count(Invoice.id)).scalar()
    total_payments = db.query(func.count(Payment.id)).scalar()
    
    # Calculate revenue statistics
    total_revenue = db.query(func.sum(Payment.amount)).scalar() or 0
    pending_invoices = db.query(func.count(Invoice.id)).filter(Invoice.status == 'draft').scalar()
    
    stats = {
        'total_clients': total_clients,
        'total_invoices': total_invoices,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'pending_invoices': pending_invoices
    }
    
    return templates.TemplateResponse("reports/dashboard.html", {
        "request": request,
        "user": current_user,
        "stats": stats,
        "title": "Reports"
    })

@router.get("/invoices", response_class=HTMLResponse)
async def invoice_reports(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice reports"""
    return templates.TemplateResponse("reports/invoices.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Reports"
    })

@router.get("/payments", response_class=HTMLResponse)
async def payment_reports(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show payment reports"""
    return templates.TemplateResponse("reports/payments.html", {
        "request": request,
        "user": current_user,
        "title": "Payment Reports"
    })

@router.get("/clients", response_class=HTMLResponse)
async def client_reports(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show client reports"""
    return templates.TemplateResponse("reports/clients.html", {
        "request": request,
        "user": current_user,
        "title": "Client Reports"
    })
