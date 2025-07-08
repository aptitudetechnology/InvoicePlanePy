from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.api_key import ApiKey


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Move the POST /invoices route here, after router is defined
@router.post("/invoices", response_class=HTMLResponse)
async def save_invoice_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    default_invoice_group: str = Form(None),
    default_payment_method: str = Form(None),
    default_terms: str = Form(None),
    invoices_due_after: int = Form(None),
    generate_invoice_number_draft: str = Form(None),
    mark_invoices_sent_pdf: str = Form(None),
    enable_pdf_watermarks: str = Form(None),
    invoice_pdf_password: str = Form(None),
    include_zugferd: str = Form(None),
    default_pdf_template: str = Form(None)
    # Add other fields as needed
):
    """Save invoice settings"""
    # TODO: Save settings to the database or config file
    # For now, just reload the page with a success message
    settings = {
        "default_invoice_group": default_invoice_group,
        "default_payment_method": default_payment_method,
        "default_terms": default_terms,
        "invoices_due_after": invoices_due_after,
        "generate_invoice_number_draft": generate_invoice_number_draft,
        "mark_invoices_sent_pdf": mark_invoices_sent_pdf,
        "enable_pdf_watermarks": enable_pdf_watermarks,
        "invoice_pdf_password": invoice_pdf_password,
        "include_zugferd": include_zugferd,
        "default_pdf_template": default_pdf_template
    }
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "settings": settings,
        "success_message": "Settings saved successfully. (Not yet persisted)"
    })

@router.get("/", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show settings page"""
    return templates.TemplateResponse("settings/index.html", {
        "request": request,
        "user": current_user,
        "title": "Settings"
    })

@router.get("/company", response_class=HTMLResponse)
async def company_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show company settings"""
    # Add default settings for the template
    settings = {
        "language": "english",
        "company_name": "",
        "company_address": "",
        # Add other fields that company.html expects
    }
    
    return templates.TemplateResponse("settings/company.html", {
        "request": request,
        "user": current_user,
        "settings": settings,  # This is what was missing!
        "title": "Company Settings"
    })

@router.get("/users", response_class=HTMLResponse)
async def user_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show user management"""
    users = db.query(User).all()
    return templates.TemplateResponse("settings/users.html", {
        "request": request,
        "user": current_user,
        "users": users,
        "title": "User Management"
    })

@router.get("/invoice", response_class=HTMLResponse)
async def invoice_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice settings"""
    # Define default settings for the invoice template, or fetch from DB if applicable
    invoice_settings_data = {
        "language": "english", # Example: Default language setting
        "invoice_prefix": "INV-",
        "invoice_start_number": 1,
        "due_days": 30,
        # Add any other settings your invoice.html template expects
    }

    # If you have actual invoice settings stored in your database (e.g., in a SystemSettings table or UserSettings related to invoices), you would fetch them here
    # For example:
    # invoice_db_settings = db.query(InvoiceSettingsModel).filter(...).first()
    # if invoice_db_settings:
    #     invoice_settings_data.update(invoice_db_settings.__dict__) # Or map relevant fields

    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "settings": invoice_settings_data, # <--- THIS IS THE FIX
        "title": "Invoice Settings"
    })

@router.post("/invoices", response_class=HTMLResponse)
async def save_invoice_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    default_invoice_group: str = Form(None),
    default_payment_method: str = Form(None),
    default_terms: str = Form(None),
    invoices_due_after: int = Form(None),
    generate_invoice_number_draft: str = Form(None),
    mark_invoices_sent_pdf: str = Form(None),
    enable_pdf_watermarks: str = Form(None),
    invoice_pdf_password: str = Form(None),
    include_zugferd: str = Form(None),
    default_pdf_template: str = Form(None)
    # Add other fields as needed
):
    """Save invoice settings"""
    # TODO: Save settings to the database or config file
    # For now, just reload the page with a success message
    settings = {
        "default_invoice_group": default_invoice_group,
        "default_payment_method": default_payment_method,
        "default_terms": default_terms,
        "invoices_due_after": invoices_due_after,
        "generate_invoice_number_draft": generate_invoice_number_draft,
        "mark_invoices_sent_pdf": mark_invoices_sent_pdf,
        "enable_pdf_watermarks": enable_pdf_watermarks,
        "invoice_pdf_password": invoice_pdf_password,
        "include_zugferd": include_zugferd,
        "default_pdf_template": default_pdf_template
    }
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "settings": settings,
        "success_message": "Settings saved successfully. (Not yet persisted)"
    })

@router.get("/custom-fields", response_class=HTMLResponse)
async def custom_fields(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show custom fields management"""
    return templates.TemplateResponse("settings/new_custom_field.html", {
        "request": request,
        "user": current_user,
        "title": "Custom Fields"
    })

@router.get("/email-templates", response_class=HTMLResponse)
async def email_templates(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show email templates management"""
    return templates.TemplateResponse("settings/email_templates.html", {
        "request": request,
        "user": current_user,
        "title": "Email Templates"
    })

@router.get("/invoice-groups", response_class=HTMLResponse)
async def invoice_groups(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice groups management"""
    return templates.TemplateResponse("settings/invoice_groups.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Groups"
    })

@router.get("/invoice-archive", response_class=HTMLResponse)
async def invoice_archive(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice archive settings"""
    return templates.TemplateResponse("settings/invoice_archive.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Archive"
    })

@router.get("/payment-methods", response_class=HTMLResponse)
async def payment_methods(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show payment methods management"""
    return templates.TemplateResponse("settings/payment_methods.html", {
        "request": request,
        "user": current_user,
        "title": "Payment Methods"
    })

@router.get("/tax-rates", response_class=HTMLResponse)
async def tax_rates(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show tax rates management"""
    return templates.TemplateResponse("settings/tax_rates.html", {
        "request": request,
        "user": current_user,
        "title": "Tax Rates"
    })

@router.get("/system", response_class=HTMLResponse)
async def system_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show system settings"""
    # Get user's API keys
    api_keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()
    
    return templates.TemplateResponse("settings/system.html", {
        "request": request,
        "user": current_user,
        "api_keys": api_keys,
        "title": "System Settings"
    })

@router.get("/import", response_class=HTMLResponse)
async def import_data(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show data import functionality"""
    return templates.TemplateResponse("settings/import.html", {
        "request": request,
        "user": current_user,
        "title": "Import Data"
    })

# API Key management endpoints
@router.post("/api/generate-key")
async def generate_api_key(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a new API key"""
    import secrets
    import hashlib
    
    # Generate a secure random key
    raw_key = f"sk_{secrets.token_urlsafe(32)}"
    
    # Hash the key for storage
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    # Create the API key record
    api_key = ApiKey(
        key_hash=key_hash,
        key_prefix=raw_key[:8],  # Store first 8 chars for display
        name="Generated from Settings",
        user_id=current_user.id
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    return JSONResponse({
        "success": True,
        "key": raw_key,
        "message": "API key generated successfully"
    })

@router.get("/api/keys")
async def list_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's API keys"""
    keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()
    return JSONResponse({
        "keys": [
            {
                "id": key.id,
                "name": key.name,
                "prefix": key.key_prefix,
                "is_active": key.is_active,
                "created_at": key.created_at.isoformat() if key.created_at else None,
                "last_used_at": key.last_used_at.isoformat() if key.last_used_at else None
            }
            for key in keys
        ]
    })

@router.delete("/api/keys/{key_id}")
async def delete_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an API key"""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    db.delete(api_key)
    db.commit()
    
    return JSONResponse({"success": True, "message": "API key deleted"})