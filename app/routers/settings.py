from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.api_key import ApiKey

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Settings"
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
