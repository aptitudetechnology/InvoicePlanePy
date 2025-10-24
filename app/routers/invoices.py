from fastapi import APIRouter, Depends, Request, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, asc, desc
import logging
from datetime import datetime, date
import secrets
import traceback

from app.database import get_db
from app.models.user import User
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
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


@router.get("/create", response_class=HTMLResponse)
async def create_invoice(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    clients = db.query(Client).all()
    current_date = date.today().isoformat()
    return templates.TemplateResponse("invoices/create.html", {
        "request": request,
        "user": current_user,
        "clients": clients,
        "current_date": current_date
    })

@router.post("/create", response_class=HTMLResponse)
async def invoice_create_post_redirect(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    client_id: int = Form(...),
    invoice_number: str = Form(None),
    status: str = Form(None),
    invoice_date: str = Form(None),
    due_date: str = Form(None),
    payment_method: str = Form(None),
    invoice_terms: str = Form(None)
    # Add other fields as needed
):
    """Handle invoice creation form submission from /create URL"""
    # Redirect to the main create post handler
    return await invoice_create_post(
        request, db, current_user, client_id, invoice_number, status, 
        invoice_date, due_date, payment_method, invoice_terms
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
    client_id: int = Form(None),
    invoice_number: str = Form(None),
    status: str = Form(None),
    invoice_date: str = Form(None),
    due_date: str = Form(None),
    payment_method: str = Form(None),
    discount_percentage: float = Form(0),
    discount_amount: float = Form(0),
    terms: str = Form(None),
    notes: str = Form(None),
    items_count: int = Form(1),
):
    """Handle invoice edit form submission"""
    try:
        logging.info(f"Starting invoice update for invoice_id: {invoice_id}")
        
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Check permissions
        if not current_user.is_admin and invoice.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Permission denied")

        # Parse form data
        form_data = await request.form()
        logging.info(f"Form data keys: {list(form_data.keys())}")

        # Update basic invoice fields
        if client_id:
            invoice.client_id = client_id
        if invoice_number:
            invoice.invoice_number = invoice_number

        # Update status
        if status:
            status_map = {
                'draft': InvoiceStatus.DRAFT.value,
                'sent': InvoiceStatus.SENT.value,
                'viewed': InvoiceStatus.VIEWED.value,
                'paid': InvoiceStatus.PAID.value,
                'overdue': InvoiceStatus.OVERDUE.value,
                'cancelled': InvoiceStatus.CANCELLED.value
            }
            invoice.status = status_map.get(status, InvoiceStatus.DRAFT.value)

        # Update dates
        if invoice_date:
            invoice.issue_date = datetime.strptime(invoice_date, "%Y-%m-%d").date()
        if due_date:
            invoice.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        # Update other fields
        invoice.discount_percentage = discount_percentage or 0
        invoice.discount_amount = discount_amount or 0
        invoice.terms = terms
        invoice.notes = notes

        # Delete existing items
        db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()

        # Process invoice items
        subtotal = 0
        tax_total = 0
        item_count = 0

        for i in range(items_count):
            item_name = form_data.get(f"item_name_{i}")
            if not item_name or not item_name.strip():  # Skip empty rows
                continue

            item_description = form_data.get(f"item_description_{i}", "")
            item_quantity_str = form_data.get(f"item_quantity_{i}", "1")
            item_price_str = form_data.get(f"item_price_{i}", "0")
            item_discount_str = form_data.get(f"item_discount_{i}", "0")
            item_tax_rate_str = form_data.get(f"item_tax_rate_{i}", "0")

            try:
                item_quantity = float(item_quantity_str) if item_quantity_str else 1
                item_price = float(item_price_str) if item_price_str else 0
                item_discount = float(item_discount_str) if item_discount_str else 0
                item_tax_rate = float(item_tax_rate_str) if item_tax_rate_str else 0
            except ValueError as e:
                logging.error(f"Error parsing item {i} values: quantity={item_quantity_str}, price={item_price_str}, discount={item_discount_str}, tax_rate={item_tax_rate_str}")
                continue

            # Calculate item totals
            item_subtotal = item_quantity * item_price
            item_tax_amount = (item_subtotal - item_discount) * (item_tax_rate / 100)
            item_total = item_subtotal - item_discount + item_tax_amount

            # Create new invoice item
            invoice_item = InvoiceItem(
                invoice_id=invoice_id,
                name=item_name.strip(),
                description=item_description.strip() if item_description else None,
                quantity=item_quantity,
                price=item_price,
                discount_amount=item_discount,
                subtotal=item_subtotal,
                tax_amount=item_tax_amount,
                total=item_total,
                order=i
            )

            # Try to link to product if item_id is provided
            item_id = form_data.get(f"item_id_{i}")
            if item_id and item_id.isdigit() and int(item_id) > 0:
                invoice_item.product_id = int(item_id)

            db.add(invoice_item)
            item_count += 1

            # Accumulate totals
            subtotal += item_subtotal
            tax_total += item_tax_amount

        logging.info(f"Processed {item_count} invoice items, subtotal: {subtotal}, tax_total: {tax_total}")

        # Calculate final totals
        discount_total = 0
        if discount_percentage > 0:
            discount_total = subtotal * (discount_percentage / 100)
        else:
            discount_total = discount_amount

        total = subtotal + tax_total - discount_total

        # Update invoice totals
        invoice.subtotal = subtotal
        invoice.tax_total = tax_total
        invoice.discount_amount = discount_total
        invoice.total = total
        invoice.balance = total - (invoice.paid_amount or 0)

        logging.info(f"Final totals - subtotal: {subtotal}, tax_total: {tax_total}, discount: {discount_total}, total: {total}, balance: {invoice.balance}")

        # Commit changes
        db.commit()
        logging.info(f"Successfully updated invoice {invoice_id}")

        # Redirect back to invoice view
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=f"/invoices/{invoice_id}", status_code=303)

    except Exception as e:
        db.rollback()
        logging.error(f"Error updating invoice {invoice_id}: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error updating invoice: {str(e)}")


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

# Moved to before /{invoice_id} route

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
    invoice_terms: str = Form(None)
    # Add other fields as needed
):
    """Handle invoice creation form submission"""
    try:
        # Parse dates
        issue_date_parsed = None
        if invoice_date:
            issue_date_parsed = datetime.strptime(invoice_date, "%Y-%m-%d").date()
        else:
            issue_date_parsed = date.today()

        due_date_parsed = None
        if due_date:
            due_date_parsed = datetime.strptime(due_date, "%Y-%m-%d").date()
        else:
            # Default due date to 30 days from issue date
            from datetime import timedelta
            due_date_parsed = issue_date_parsed + timedelta(days=30)

        # Generate invoice number if not provided
        if not invoice_number:
            last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
            next_number = (last_invoice.id + 1) if last_invoice else 1
            invoice_number = f"INV-{next_number:04d}"

        # Create new invoice
        invoice = Invoice(
            invoice_number=invoice_number,
            client_id=client_id,
            user_id=current_user.id,
            issue_date=issue_date_parsed,
            due_date=due_date_parsed,
            status=1,  # Draft status (InvoiceStatus.DRAFT.value)
            total=0,  # Ensure total is never None
            balance=0,  # Ensure balance is never None - initially equals total
            subtotal=0,  # Initialize subtotal to 0
            tax_total=0,  # Initialize tax_total to 0
            discount_amount=0,  # Initialize discount_amount to 0
            terms=invoice_terms,
        )

        # Generate URL key
        invoice.url_key = secrets.token_urlsafe(24)

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        return RedirectResponse(url=f"/invoices/{invoice.id}/edit", status_code=302)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")

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


@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an invoice
    """
    # Find the invoice
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Check permissions
    if not current_user.is_admin and invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Delete the invoice (cascade will handle invoice items)
    try:
        db.delete(invoice)
        db.commit()
        return {"message": f"Invoice {invoice.invoice_number} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete invoice: {str(e)}")


@router.post("/import")
async def import_invoices_web(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Web endpoint to trigger invoice import from legacy data.
    Requires admin privileges.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required for import")

    try:
        # Import the import function
        import subprocess
        import sys
        import os

        # Run the import script
        script_path = os.path.join(os.path.dirname(__file__), "..", "..", "importdb", "import_legacy_data.py")
        result = subprocess.run([
            sys.executable, script_path, "--table", "invoices"
        ], capture_output=True, text=True, cwd=os.path.dirname(script_path))

        if result.returncode == 0:
            # Import successful, now verify the data
            verification = await verify_imported_invoices(db)
            return {
                "message": "Import completed successfully",
                "import_output": result.stdout,
                "verification": verification
            }
        else:
            return {
                "error": "Import failed",
                "stdout": result.stdout,
                "stderr": result.stderr
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/verify-import")
async def verify_imported_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Verify that imported invoices have all required fields populated.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    try:
        # Get all invoices with their items
        invoices = db.query(Invoice).options(
            joinedload(Invoice.items)
        ).all()

        verification_results = {
            "total_invoices": len(invoices),
            "invoices_with_items": 0,
            "invoices_with_totals": 0,
            "issues": [],
            "sample_invoices": []
        }

        for invoice in invoices[:5]:  # Check first 5 invoices as samples
            invoice_status = {
                "id": invoice.id,
                "number": invoice.invoice_number,
                "has_items": len(invoice.items) > 0,
                "has_totals": all([
                    invoice.subtotal is not None,
                    invoice.total is not None,
                    invoice.balance is not None
                ]),
                "items": []
            }

            if invoice.items:
                verification_results["invoices_with_items"] += 1

            if invoice_status["has_totals"]:
                verification_results["invoices_with_totals"] += 1

            # Check each item
            for item in invoice.items:
                item_status = {
                    "name": item.name,
                    "description": item.description,
                    "quantity": item.quantity,
                    "price": item.price,
                    "has_name": item.name and item.name.strip() != "",
                    "has_description": item.description and item.description.strip() != "",
                    "has_quantity": item.quantity is not None,
                    "has_price": item.price is not None,
                    "has_totals": all([
                        item.subtotal is not None,
                        item.total is not None
                    ])
                }
                invoice_status["items"].append(item_status)

                # Check for issues
                if not item_status["has_name"]:
                    verification_results["issues"].append(f"Invoice {invoice.invoice_number}: Item missing name")
                if not item_status["has_quantity"]:
                    verification_results["issues"].append(f"Invoice {invoice.invoice_number}: Item missing quantity")
                if not item_status["has_price"]:
                    verification_results["issues"].append(f"Invoice {invoice.invoice_number}: Item missing price")

            verification_results["sample_invoices"].append(invoice_status)

        # Overall assessment
        if verification_results["total_invoices"] == 0:
            verification_results["status"] = "no_invoices"
        elif len(verification_results["issues"]) == 0 and verification_results["invoices_with_items"] == verification_results["total_invoices"]:
            verification_results["status"] = "success"
        else:
            verification_results["status"] = "issues_found"

        return verification_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@router.get("/import", response_class=HTMLResponse)
async def import_invoices_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """
    Web page for invoice import operations.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    return templates.TemplateResponse(
        "invoices/import.html",
        {
            "request": request,
            "user": current_user,
            "title": "Import Invoices"
        }
    )

@router.post("/{invoice_id}")
async def handle_invalid_invoice_post(invoice_id: str):
    """Handle POST requests to invalid invoice IDs"""
    raise HTTPException(status_code=404, detail="Invoice not found")

