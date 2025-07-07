from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models.user import User
from ..models.client import Client
from ..models.invoice import Invoice, InvoiceStatus
from ..dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get dashboard statistics
    stats = await get_dashboard_stats(db, current_user)
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request, 
            "user": current_user,
            "stats": stats
        }
    )

async def get_dashboard_stats(db: Session, user: User) -> dict:
    """Get dashboard statistics"""
    
    # Base query filters based on user role
    invoice_query = db.query(Invoice)
    client_query = db.query(Client)
    
    if not user.is_admin:
        invoice_query = invoice_query.filter(Invoice.user_id == user.id)
        # For now, all users can see all clients (adjust as needed)
    
    # Invoice statistics
    total_invoices = invoice_query.count()
    draft_invoices = invoice_query.filter(Invoice.status == InvoiceStatus.DRAFT).count()
    sent_invoices = invoice_query.filter(Invoice.status == InvoiceStatus.SENT).count()
    paid_invoices = invoice_query.filter(Invoice.status == InvoiceStatus.PAID).count()
    overdue_invoices = invoice_query.filter(Invoice.status == InvoiceStatus.OVERDUE).count()
    
    # Financial statistics
    total_revenue = invoice_query.filter(Invoice.status == InvoiceStatus.PAID).with_entities(
        func.sum(Invoice.total)
    ).scalar() or 0
    
    outstanding_amount = invoice_query.filter(
        Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.VIEWED, InvoiceStatus.OVERDUE])
    ).with_entities(func.sum(Invoice.balance)).scalar() or 0
    
    # Client statistics
    total_clients = client_query.count()
    active_clients = client_query.filter(Client.is_active == True).count()
    
    # Recent invoices (last 5)
    recent_invoices = invoice_query.order_by(Invoice.created_at.desc()).limit(5).all()
    
    return {
        "invoices": {
            "total": total_invoices,
            "draft": draft_invoices,
            "sent": sent_invoices,
            "paid": paid_invoices,
            "overdue": overdue_invoices
        },
        "financial": {
            "total_revenue": float(total_revenue),
            "outstanding": float(outstanding_amount)
        },
        "clients": {
            "total": total_clients,
            "active": active_clients
        },
        "recent_invoices": recent_invoices
    }
