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

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def quotes_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all quotes"""
    # Get quotes based on user role (matching invoice pattern)
    query = db.query(Quote)
    if not current_user.is_admin:
        query = query.filter(Quote.user_id == current_user.id)
    
    quotes = query.order_by(Quote.created_at.desc()).all()
    
    return templates.TemplateResponse("quotes/list.html", {
        "request": request,
        "user": current_user,
        "quotes": quotes
    })

@router.get("/create", response_class=HTMLResponse)
async def create_quote(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create quote form"""
    clients = db.query(Client).all()
    return templates.TemplateResponse("quotes/create.html", {
        "request": request,
        "user": current_user,
        "clients": clients
    })

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
    terms: str = Form(None),
    notes: str = Form(None)
):
    """Handle quote creation (matching invoice pattern)"""
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
            # Simple auto-generation - you might want to customize this
            last_quote = db.query(Quote).order_by(Quote.id.desc()).first()
            next_number = (last_quote.id + 1) if last_quote else 1
            quote_number = f"QUO-{next_number:04d}"
        
        # Parse status
        quote_status = QuoteStatus.DRAFT
        if status:
            try:
                quote_status = QuoteStatus(status)
            except ValueError:
                quote_status = QuoteStatus.DRAFT
        
        # Create new quote
        quote = Quote(
            quote_number=quote_number,
            client_id=client_id,
            user_id=current_user.id,
            issue_date=issue_date_parsed,
            valid_until=valid_until_parsed,
            status=quote_status,
            terms=terms,
            notes=notes
        )
        
        # Generate URL key (similar to invoice pattern)
        import secrets
        quote.url_key = secrets.token_urlsafe(24)
        
        db.add(quote)
        db.commit()
        db.refresh(quote)
        
        #return RedirectResponse(url=f"/quotes/{quote.id}", status_code=302)
        return RedirectResponse(url=f"/quotes/{quote.id}/edit", status_code=302)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating quote: {str(e)}")

@router.get("/{quote_id}", response_class=HTMLResponse)
async def view_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific quote"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Check permissions (matching invoice pattern)
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return templates.TemplateResponse("quotes/view.html", {
        "request": request,
        "user": current_user,
        "quote": quote,
        "title": f"Quote #{quote.quote_number}"
    })

@router.get("/{quote_id}/edit", response_class=HTMLResponse)
async def edit_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show edit quote form"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    clients = db.query(Client).all()
    
    return templates.TemplateResponse("quotes/edit.html", {
        "request": request,
        "user": current_user,
        "quote": quote,
        "clients": clients,
        "quote_statuses": QuoteStatus,
        "title": f"Edit Quote #{quote.quote_number}"
    })

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
    terms: str = Form(None),
    notes: str = Form(None)
):
    """Handle quote editing"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    try:
        # Update quote fields
        quote.client_id = client_id
        quote.quote_number = quote_number
        quote.status = QuoteStatus(status)
        quote.terms = terms
        quote.notes = notes
        
        # Parse and update dates
        if issue_date:
            quote.issue_date = datetime.strptime(issue_date, "%Y-%m-%d").date()
        
        if valid_until:
            quote.valid_until = datetime.strptime(valid_until, "%Y-%m-%d").date()
        else:
            quote.valid_until = None
        
        # Update timestamp (BaseModel should handle this automatically)
        quote.updated_at = datetime.utcnow()
        
        db.commit()
        
        return RedirectResponse(url=f"/quotes/{quote.id}", status_code=302)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating quote: {str(e)}")

@router.post("/{quote_id}/delete")
async def delete_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

@router.post("/{quote_id}/convert")
async def convert_quote_to_invoice(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Convert accepted quote to invoice"""
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Check permissions
    if not current_user.is_admin and quote.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Check if quote can be converted
    if not quote.can_be_converted:
        raise HTTPException(status_code=400, detail="Quote cannot be converted. It must be accepted first.")
    
    try:
        # You'll need to implement this based on your Invoice model
        # This is a placeholder for the conversion logic
        from app.models.invoice import Invoice, InvoiceStatus
        
        # Generate invoice number
        last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
        next_number = (last_invoice.id + 1) if last_invoice else 1
        invoice_number = f"INV-{next_number:04d}"
        
        # Create invoice from quote
        invoice = Invoice(
            invoice_number=invoice_number,
            client_id=quote.client_id,
            user_id=quote.user_id,
            issue_date=date.today(),
            due_date=date.today(),  # You might want to calculate this
            status=InvoiceStatus.DRAFT,
            terms=quote.terms,
            notes=quote.notes,
            subtotal=quote.subtotal,
            tax_total=quote.tax_total,
            total=quote.total
        )
        
        # Generate URL key
        import secrets
        invoice.url_key = secrets.token_urlsafe(24)
        
        db.add(invoice)
        
        # Update quote status
        quote.status = QuoteStatus.CONVERTED
        
        db.commit()
        db.refresh(invoice)
        
        return RedirectResponse(url=f"/invoices/{invoice.id}", status_code=302)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error converting quote: {str(e)}")

@router.get("/{quote_id}/duplicate", response_class=HTMLResponse)
async def duplicate_quote(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
            terms=quote.terms,
            notes=quote.notes,
            subtotal=quote.subtotal,
            tax_total=quote.tax_total,
            total=quote.total
        )
        
        # Generate URL key
        import secrets
        new_quote.url_key = secrets.token_urlsafe(24)
        
        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)
        
        return RedirectResponse(url=f"/quotes/{new_quote.id}", status_code=302)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error duplicating quote: {str(e)}")