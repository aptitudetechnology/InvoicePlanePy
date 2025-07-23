from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.client import Client
from app.models.quotes import Quote, QuoteStatus
from datetime import date, datetime
from sqlalchemy.orm import joinedload
from datetime import timedelta
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
import secrets

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def parse_quote_status(status_str: str) -> QuoteStatus:
    """
    Parse status string to QuoteStatus enum with fallback handling
    """
    if not status_str:
        return QuoteStatus.DRAFT
    
    # Try direct match first
    try:
        return QuoteStatus(status_str)
    except ValueError:
        pass
    
    # Try uppercase
    try:
        return QuoteStatus(status_str.upper())
    except ValueError:
        pass
    
    # Try mapping common variations
    status_mapping = {
        'approved': QuoteStatus.ACCEPTED,
        'approve': QuoteStatus.ACCEPTED,
        'accept': QuoteStatus.ACCEPTED,
        'accepted': QuoteStatus.ACCEPTED,
        'draft': QuoteStatus.DRAFT,
        'sent': QuoteStatus.SENT,
        'send': QuoteStatus.SENT,
        'viewed': QuoteStatus.VIEWED,
        'view': QuoteStatus.VIEWED,
        'rejected': QuoteStatus.REJECTED,
        'reject': QuoteStatus.REJECTED,
        'expired': QuoteStatus.EXPIRED,
        'expire': QuoteStatus.EXPIRED,
        'converted': QuoteStatus.CONVERTED,
        'convert': QuoteStatus.CONVERTED,
    }
    
    mapped_status = status_mapping.get(status_str.lower())
    if mapped_status:
        return mapped_status
    
    # If all else fails, return DRAFT
    print(f"Warning: Could not parse status '{status_str}', defaulting to DRAFT")
    return QuoteStatus.DRAFT


@router.get("/", response_class=HTMLResponse)
async def quotes_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all quotes"""
    query = db.query(Quote)
    if not current_user.is_admin:
        query = query.filter(Quote.user_id == current_user.id)

    quotes = query.order_by(Quote.created_at.desc()).all()

    return templates.TemplateResponse(
        "quotes/list.html", {"request": request, "user": current_user, "quotes": quotes}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_quote(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Show create quote form"""
    clients = db.query(Client).all()
    return templates.TemplateResponse(
        "quotes/create.html",
        {"request": request, "user": current_user, "clients": clients, "quote_statuses": QuoteStatus},
    )


@router.post("/create", response_class=HTMLResponse)
async def quote_create_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    client_id: int = Form(...),
    quote_number: str = Form(None),
    status: str = Form(None),
    issue_date: str = Form(None),
    valid_until: str = Form(None),
    notes: str = Form(None),
):
    """Handle quote creation with improved enum handling"""
    try:
        # Parse dates
        issue_date_parsed = None
        if issue_date:
            issue_date_parsed = datetime.strptime(issue_date, "%Y-%m-%d").date()
        else:
            issue_date_parsed = date.today()

        valid_until_parsed = None
        if valid_until:
            valid_until_parsed = datetime.strptime(valid_until, "%Y-%m-%d").date()

        # Generate quote number if not provided
        if not quote_number:
            last_quote = db.query(Quote).order_by(Quote.id.desc()).first()
            next_number = (last_quote.id + 1) if last_quote else 1
            quote_number = f"QUO-{next_number:04d}"

        # Parse status with fallback handling
        quote_status = parse_quote_status(status)
        from app.utils.status_helpers import get_status_id
        status_id = get_status_id(db, quote_status)

        # Create new quote
        quote = Quote(
            quote_number=quote_number,
            client_id=client_id,
            user_id=current_user.id,
            issue_date=issue_date_parsed,
            valid_until=valid_until_parsed,
            status=status_id,
            #terms=None,  # terms is not settable here; use default or config elsewhere
            notes=notes,
        )

        # Generate URL key
        quote.url_key = secrets.token_urlsafe(24)

        db.add(quote)
        db.commit()
        db.refresh(quote)

        return RedirectResponse(url=f"/quotes/{quote.id}/edit", status_code=302)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating quote: {str(e)}")


@router.get("/{quote_id}", response_class=HTMLResponse)
async def view_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """View a specific quote"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return templates.TemplateResponse(
        "quotes/view.html",
        {
            "request": request,
            "user": current_user,
            "quote": quote,
            "title": f"Quote #{quote.quote_number}",
        },
    )


@router.get("/{quote_id}/edit", response_class=HTMLResponse)
async def edit_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Show edit quote form"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    clients = db.query(Client).all()

    return templates.TemplateResponse(
        "quotes/edit.html",
        {
            "request": request,
            "user": current_user,
            "quote": quote,
            "clients": clients,
            "quote_statuses": QuoteStatus,
            "title": f"Edit Quote #{quote.quote_number}",
        },
    )


@router.post("/{quote_id}/edit")
async def edit_quote_post(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    client_id: int = Form(...),
    quote_number: str = Form(...),
    status: str = Form(...),
    issue_date: str = Form(...),
    valid_until: str = Form(None),
    notes: str = Form(None),
):
    """Handle quote editing with improved enum handling"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        # Store original values for debugging
        original_status = quote.status
        print(f"Updating quote {quote_id}: {original_status} -> {status}")

        # Update quote fields
        quote.client_id = client_id
        quote.quote_number = quote_number
        
        # Use improved status parsing
        quote_status = parse_quote_status(status)
        from app.utils.status_helpers import get_status_id
        quote.status = get_status_id(db, quote_status)
        print(f"Parsed status: {quote.status}")
        
        quote.notes = notes

        # Parse and update dates
        if issue_date:
            quote.issue_date = datetime.strptime(issue_date, "%Y-%m-%d").date()

        if valid_until:
            quote.valid_until = datetime.strptime(valid_until, "%Y-%m-%d").date()
        else:
            quote.valid_until = None

        # Update timestamp
        quote.updated_at = datetime.utcnow()

        db.commit()
        print(f"Quote {quote_id} updated successfully")

        return RedirectResponse(url=f"/quotes/{quote.id}", status_code=302)

    except Exception as e:
        db.rollback()
        print(f"Error updating quote {quote_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating quote: {str(e)}")


@router.post("/{quote_id}/delete")
async def delete_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a quote"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        db.delete(quote)
        db.commit()
        return RedirectResponse(url="/quotes", status_code=302)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting quote: {str(e)}")


@router.get("/{quote_id}/convert-to-invoice")
async def convert_quote_to_invoice(
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Convert accepted quote to invoice"""
    quote = (
        db.query(Quote)
        .options(joinedload(Quote.client), joinedload(Quote.items))
        .filter(Quote.id == quote_id)
        .first()
    )

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Check permissions
    if quote.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to convert this quote"
        )

    # Check if quote is in a valid state to convert
    if quote.status not in [QuoteStatus.ACCEPTED, QuoteStatus.SENT]:
        raise HTTPException(
            status_code=400,
            detail="Quote must be accepted or sent before converting to invoice",
        )

    try:
        # Generate invoice number
        latest_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
        if latest_invoice and latest_invoice.invoice_number:
            last_num = (
                int(latest_invoice.invoice_number.split("-")[-1])
                if "-" in latest_invoice.invoice_number
                else int(latest_invoice.invoice_number)
            )
            invoice_number = f"INV-{last_num + 1:04d}"
        else:
            invoice_number = "INV-0001"

        # Create new invoice from quote
        invoice = Invoice(
            client_id=quote.client_id,
            user_id=current_user.id,
            invoice_number=invoice_number,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            status="draft",
            #terms=quote.terms,
            #tems=quote.notes,
            subtotal=quote.subtotal or 0,
            tax_amount=quote.tax_amount or 0,
            discount_amount=quote.discount_amount or 0,
            total=quote.total or 0,
            discount_percentage=quote.discount_percentage or 0,
            tax_rate=quote.tax_rate or 0,
            currency=quote.currency or "USD",
            reference_quote_id=quote.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(invoice)
        db.flush()

        # Copy items from quote to invoice
        for item in quote.items:
            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                name=item.name,
                description=item.description,
                quantity=item.quantity or 1,
                price=item.price or 0,
                discount=item.discount or 0,
                tax_rate=item.tax_rate or 0,
                subtotal=item.subtotal or 0,
                discount_amount=item.discount_amount or 0,
                tax_amount=item.tax_amount or 0,
                total=item.total or 0,
                unit=item.unit if hasattr(item, "unit") else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(invoice_item)

        # Update quote status to converted
        quote.status = QuoteStatus.CONVERTED
        quote.converted_to_invoice_id = invoice.id
        quote.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(invoice)

        return RedirectResponse(url=f"/invoices/{invoice.id}", status_code=302)

    except Exception as e:
        db.rollback()
        print(f"Error converting quote to invoice: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while converting the quote to invoice",
        )


@router.post("/{quote_id}/convert-to-invoice")
async def convert_quote_to_invoice_post(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """POST version for form submission with confirmation"""
    try:
        return await convert_quote_to_invoice(quote_id, db, current_user)
    except HTTPException as e:
        return RedirectResponse(
            url=f"/quotes/{quote_id}?error={e.detail}", status_code=302
        )


@router.get("/{quote_id}/duplicate", response_class=HTMLResponse)
async def duplicate_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Duplicate an existing quote"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        # Generate new quote number
        last_quote = db.query(Quote).order_by(Quote.id.desc()).first()
        next_number = (last_quote.id + 1) if last_quote else 1
        new_quote_number = f"QUO-{next_number:04d}"

        # Create duplicate quote
        new_quote = Quote(
            quote_number=new_quote_number,
            client_id=quote.client_id,
            user_id=current_user.id,
            issue_date=date.today(),
            valid_until=quote.valid_until,
            status=QuoteStatus.DRAFT,
            #erms=quote.terms,
            notes=quote.notes,
            subtotal=quote.subtotal,
            tax_total=quote.tax_total,
            total=quote.total,
        )

        # Generate URL key
        new_quote.url_key = secrets.token_urlsafe(24)

        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)

        return RedirectResponse(url=f"/quotes/{new_quote.id}", status_code=302)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error duplicating quote: {str(e)}"
        )


# Helper function to validate quote conversion eligibility
def can_convert_quote_to_invoice(quote: Quote) -> tuple[bool, str]:
    """
    Check if a quote can be converted to an invoice
    Returns (can_convert, reason)
    """
    if not quote:
        return False, "Quote not found"

    if quote.status == QuoteStatus.CONVERTED:
        return False, "Quote has already been converted to an invoice"

    if quote.status not in [QuoteStatus.ACCEPTED, QuoteStatus.SENT]:
        return False, "Quote must be accepted or sent before converting"

    if not hasattr(quote, 'items') or not quote.items:
        return False, "Quote must have at least one item"

    if not quote.client_id:
        return False, "Quote must have a client assigned"

    # Check if quote is expired
    if quote.valid_until and quote.valid_until < date.today():
        return False, "Quote has expired and cannot be converted"

    return True, "Quote can be converted"