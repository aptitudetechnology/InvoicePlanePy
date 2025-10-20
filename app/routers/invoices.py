from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, asc, desc
import logging

from app.database import get_db
from app.models.user import User
from app.models.invoice import Invoice, InvoiceItem
from app.models.client import Client
from app.models.invoicesettings import InvoiceSettings
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/api")
async def get_invoices_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    search: str = Query(None, description="Search invoices by number, client name, or notes"),
    status: str = Query(None, description="Filter by status: draft, sent, viewed, paid, overdue, cancelled"),
    sort_by: str = Query("created_at", description="Sort by: created_at, issue_date, due_date, total, invoice_number"),
    sort_order: str = Query("desc", description="Sort order: asc or desc")
):
    """
    Get paginated list of invoices with full details including items and client information.
    Returns JSON data for API integration.
    """
    try:
        offset = (page - 1) * limit

        # Base query with eager loading of related data
        invoices_query = db.query(Invoice).options(
            joinedload(Invoice.client),
            joinedload(Invoice.items).joinedload(InvoiceItem.product),
            joinedload(Invoice.user)
        )

        # Apply user filter (non-admin users only see their own invoices)
        if not current_user.is_admin:
            invoices_query = invoices_query.filter(Invoice.user_id == current_user.id)

        # Apply status filter if provided
        if status:
            status_map = {
                'draft': 1, 'sent': 2, 'viewed': 3, 'paid': 4, 'overdue': 5, 'cancelled': 6
            }
            if status in status_map:
                invoices_query = invoices_query.filter(Invoice.status == status_map[status])

        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            invoices_query = invoices_query.filter(
                or_(
                    Invoice.invoice_number.ilike(search_term),
                    Invoice.notes.ilike(search_term),
                    Invoice.terms.ilike(search_term),
                    Invoice.client.has(Client.name.ilike(search_term)) if hasattr(Client, 'name') else True
                )
            )

        # Apply sorting
        sort_column = None
        if sort_by == "created_at":
            sort_column = Invoice.created_at
        elif sort_by == "issue_date":
            sort_column = Invoice.issue_date
        elif sort_by == "due_date":
            sort_column = Invoice.due_date
        elif sort_by == "total":
            sort_column = Invoice.total
        elif sort_by == "invoice_number":
            sort_column = Invoice.invoice_number
        else:
            sort_column = Invoice.created_at  # Default fallback

        if sort_order.lower() == "desc":
            invoices_query = invoices_query.order_by(desc(sort_column))
        else:
            invoices_query = invoices_query.order_by(asc(sort_column))

        # Get paginated results
        invoices = invoices_query.offset(offset).limit(limit).all()

        # Get total count for pagination
        total_query = db.query(Invoice)
        if not current_user.is_admin:
            total_query = total_query.filter(Invoice.user_id == current_user.id)
        if status:
            if status in status_map:
                total_query = total_query.filter(Invoice.status == status_map[status])
        if search:
            search_term = f"%{search}%"
            total_query = total_query.filter(
                or_(
                    Invoice.invoice_number.ilike(search_term),
                    Invoice.notes.ilike(search_term),
                    Invoice.terms.ilike(search_term),
                    Invoice.client.has(Client.name.ilike(search_term)) if hasattr(Client, 'name') else True
                )
            )
        total_invoices = total_query.count()

        # Format invoices data with full details
        invoices_data = []
        for invoice in invoices:
            # Client information
            client_data = None
            if invoice.client:
                client_data = {
                    "id": invoice.client.id,
                    "name": getattr(invoice.client, 'name', None) or f"{getattr(invoice.client, 'client_name', '')} {getattr(invoice.client, 'client_surname', '')}".strip(),
                    "email": getattr(invoice.client, 'email', None) or getattr(invoice.client, 'client_email', None),
                    "address": getattr(invoice.client, 'address_1', None)
                }

            # Invoice items
            items_data = []
            for item in invoice.items:
                product_data = None
                if item.product:
                    product_data = {
                        "id": item.product.id,
                        "name": item.product.name,
                        "sku": item.product.sku
                    }

                items_data.append({
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "quantity": float(item.quantity) if item.quantity is not None else 0,
                    "price": float(item.price) if item.price is not None else 0,
                    "subtotal": float(item.subtotal) if item.subtotal is not None else 0,
                    "tax_amount": float(item.tax_amount) if item.tax_amount is not None else 0,
                    "discount_amount": float(item.discount_amount) if item.discount_amount is not None else 0,
                    "total": float(item.total) if item.total is not None else 0,
                    "product": product_data
                })

            # Status name
            status_names = {
                1: 'draft', 2: 'sent', 3: 'viewed', 4: 'paid', 5: 'overdue', 6: 'cancelled'
            }
            status_name = status_names.get(invoice.status, 'unknown')

            invoice_data = {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "status": invoice.status,
                "status_name": status_name,
                "issue_date": str(invoice.issue_date) if invoice.issue_date else None,
                "due_date": str(invoice.due_date) if invoice.due_date else None,
                "terms": invoice.terms,
                "notes": invoice.notes,
                "url_key": invoice.url_key,
                "subtotal": float(invoice.subtotal) if invoice.subtotal is not None else 0,
                "tax_total": float(invoice.tax_total) if invoice.tax_total is not None else 0,
                "discount_amount": float(invoice.discount_amount) if invoice.discount_amount is not None else 0,
                "discount_percentage": float(invoice.discount_percentage) if invoice.discount_percentage is not None else 0,
                "total": float(invoice.total) if invoice.total is not None else 0,
                "paid_amount": float(invoice.paid_amount) if invoice.paid_amount is not None else 0,
                "balance": float(invoice.balance) if invoice.balance is not None else 0,
                "is_overdue": getattr(invoice, 'is_overdue', False),
                "days_overdue": getattr(invoice, 'days_overdue', 0),
                "client": client_data,
                "items": items_data,
                "user_id": invoice.user_id,
                "created_at": invoice.created_at.isoformat() if hasattr(invoice, 'created_at') and invoice.created_at else None,
                "updated_at": invoice.updated_at.isoformat() if hasattr(invoice, 'updated_at') and invoice.updated_at else None
            }
            invoices_data.append(invoice_data)

        return {
            "invoices": invoices_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_invoices,
                "total_pages": (total_invoices + limit - 1) // limit
            },
            "filters": {
                "search": search,
                "status": status,
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        }

    except Exception as e:
        logging.error(f"Unexpected error in get_invoices_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

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


@router.get("/{invoice_id}/edit", response_class=HTMLResponse)
async def edit_invoice(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Show edit invoice form"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Check permissions
    if not current_user.is_admin and invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    clients = db.query(Client).all()
    
    # Load invoice settings
    invoice_settings = db.query(InvoiceSettings).first()
    if not invoice_settings:
        invoice_settings = InvoiceSettings()
        db.add(invoice_settings)
        db.commit()
        db.refresh(invoice_settings)

    return templates.TemplateResponse(
        "invoices/edit.html",
        {
            "request": request,
            "user": current_user,
            "invoice": invoice,
            "clients": clients,
            "invoice_settings": invoice_settings,
            "title": f"Edit Invoice #{invoice.invoice_number}",
        },
    )


@router.post("/{invoice_id}/edit")
async def edit_invoice_post(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    # Add form fields as needed
):
    """Handle invoice edit form submission"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Check permissions
    if not current_user.is_admin and invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    # For now, just redirect back to the invoice view
    # TODO: Implement actual invoice update logic
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/invoices/{invoice_id}", status_code=303)


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

@router.get("/{invoice_id}/api", response_class=JSONResponse)
async def get_invoice_api(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific invoice as JSON data"""
    from sqlalchemy.orm import joinedload
    invoice = db.query(Invoice).options(
        joinedload(Invoice.client),
        joinedload(Invoice.items).joinedload(InvoiceItem.product),
        joinedload(Invoice.user)
    ).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Check permissions
    if not current_user.is_admin and invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Convert invoice to dictionary
    invoice_data = {
        "id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "status": invoice.status,
        "status_name": invoice.status_name,
        "issue_date": invoice.issue_date.isoformat() if invoice.issue_date else None,
        "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
        "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
        "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
        "subtotal": float(invoice.subtotal or 0),
        "tax_total": float(invoice.tax_total or 0),
        "discount_amount": float(invoice.discount_amount or 0),
        "total": float(invoice.total or 0),
        "balance": float(invoice.balance or 0),
        "notes": invoice.notes,
        "terms": invoice.terms,
        "client": {
            "id": invoice.client.id,
            "name": invoice.client.name,
            "email": invoice.client.email,
            "address": invoice.client.address,
            "phone": invoice.client.phone,
        } if invoice.client else None,
        "user": {
            "id": invoice.user.id,
            "username": invoice.user.username,
            "email": invoice.user.email,
        } if invoice.user else None,
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "quantity": float(item.quantity or 0),
                "price": float(item.price or 0),
                "discount_amount": float(item.discount_amount or 0),
                "tax_amount": float(item.tax_amount or 0),
                "subtotal": float(item.subtotal or 0),
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "sku": item.product.sku,
                } if item.product else None,
            }
            for item in invoice.items
        ]
    }

    return JSONResponse(content=invoice_data)

