from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.payment import Payment
import logging

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

@router.get("/api")
async def get_payments_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    search: str = Query(None, description="Search payments by payer or reference")
):
    """
    Get paginated list of payments for the admin interface.
    Returns JSON data for dynamic table loading.
    """
    try:
        offset = (page - 1) * limit
        payments_query = db.query(Payment)
        
        if search:
            search_term = f"%{search}%"
            payments_query = payments_query.filter(
                or_(
                    Payment.payer.ilike(search_term),
                    Payment.reference.ilike(search_term)
                )
            )
        
        payments = payments_query.offset(offset).limit(limit).all()
        
        # Get total count for pagination
        total_query = db.query(Payment)
        if search:
            search_term = f"%{search}%"
            total_query = total_query.filter(
                or_(
                    Payment.payer.ilike(search_term),
                    Payment.reference.ilike(search_term)
                )
            )
        total_payments = total_query.count()
        
        payments_data = []
        for payment in payments:
            payments_data.append({
                "id": payment.id,
                "amount": float(payment.amount) if payment.amount is not None else None,
                "payer": payment.payer,
                "reference": payment.reference if payment.reference else None,
                "date": str(payment.date) if payment.date else None,
                "status": payment.status if hasattr(payment, 'status') else 'completed'
            })
        
        return {
            "payments": payments_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_payments,
                "total_pages": (total_payments + limit - 1) // limit
            }
        }
        
    except SQLAlchemyError as e:
        logging.error(f"Database error in get_payments_api: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error in get_payments_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

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