from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.invoicesettings import InvoiceSettings
import logging

# Add this at the top of your file
logger = logging.getLogger(__name__)


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
        "settings": settings,
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

@router.get("/users/create", response_class=HTMLResponse)
async def create_user(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Pass an empty user object and any other required context (e.g., languages)
    return templates.TemplateResponse("settings/create.html", {
        "request": request,
        "user": None,
        "languages": [],  # or your actual languages list
        "title": "Create User"
    })

@router.get("/invoice", response_class=HTMLResponse)
async def invoice_settings(
    request: Request, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Show invoice settings"""
    # Fetch invoice settings from database
    invoice_db_settings = db.query(InvoiceSettings).first()  # System-wide settings
    # OR if user-specific: db.query(InvoiceSettings).filter(InvoiceSettings.user_id == current_user.id).first()
    
    if invoice_db_settings:
        # Use the actual database object
        invoice_settings_data = invoice_db_settings
    else:
        # Create default settings object if none exists
        invoice_settings_data = InvoiceSettings(
            default_invoice_group="invoice-default",
            default_invoice_terms="Payment due within 30 days",
            invoice_default_payment_method="bank_transfer",
            invoices_due_after=30,
            generate_invoice_number_for_draft=False,
            einvoicing=False,
            pdf_invoice_footer="Thank you for your business",
            pdf_template="default",
            invoice_logo=None,
            invoice_pdf_password=None,
            enable_pdf_watermarks=False,
            include_zugferd=False
        )
    
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "invoice_settings": invoice_settings_data,
        "title": "Invoice Settings"
    })

@router.post("/invoice", response_class=HTMLResponse)
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
    default_pdf_template: str = Form(None),
    pdf_invoice_footer: str = Form(None)
):
    import os
    import json
    import traceback
    from pathlib import Path
    
    logger.info("=== STARTING INVOICE SETTINGS SAVE PROCESS ===")
    
    try:
        # Step 1: Log all incoming form data
        logger.info("=== FORM DATA DEBUG ===")
        form_data = {
            'default_invoice_group': default_invoice_group,
            'default_payment_method': default_payment_method,
            'default_terms': default_terms,
            'invoices_due_after': invoices_due_after,
            'generate_invoice_number_draft': generate_invoice_number_draft,
            'mark_invoices_sent_pdf': mark_invoices_sent_pdf,
            'enable_pdf_watermarks': enable_pdf_watermarks,
            'invoice_pdf_password': invoice_pdf_password,
            'include_zugferd': include_zugferd,
            'default_pdf_template': default_pdf_template,
            'pdf_invoice_footer': pdf_invoice_footer
        }
        
        for key, value in form_data.items():
            logger.info(f"Form field '{key}': {repr(value)} (type: {type(value).__name__})")
        
        # Step 2: Check database connection health
        logger.info("=== DATABASE CONNECTION CHECK ===")
        try:
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            logger.info("Database connection is healthy")
        except Exception as db_check_error:
            logger.error(f"Database connection issue: {db_check_error}")
            raise
        
        # Step 3: Query existing settings with detailed logging
        logger.info("=== QUERYING EXISTING SETTINGS ===")
        settings_obj = db.query(InvoiceSettings).first()
        
        if settings_obj:
            logger.info(f"Found existing settings record with ID: {settings_obj.id}")
            logger.info(f"Current settings object type: {type(settings_obj).__name__}")
            
            # Log current values for comparison
            logger.info("=== CURRENT SETTINGS VALUES ===")
            try:
                current_values = {
                    'id': settings_obj.id,
                    'default_invoice_group': settings_obj.default_invoice_group,
                    'default_invoice_terms': settings_obj.default_invoice_terms,
                    'invoice_default_payment_method': settings_obj.invoice_default_payment_method,
                    'invoices_due_after': settings_obj.invoices_due_after,
                    'generate_invoice_number_for_draft': settings_obj.generate_invoice_number_for_draft,
                    'einvoicing': settings_obj.einvoicing,
                    'pdf_template': settings_obj.pdf_template,
                    'pdf_invoice_footer': settings_obj.pdf_invoice_footer
                }
                for key, value in current_values.items():
                    logger.info(f"Current {key}: {repr(value)}")
            except Exception as attr_error:
                logger.error(f"Error reading current settings attributes: {attr_error}")
        else:
            logger.info("No existing settings found, will create new record")
        
        # Step 4: Perform database operations with detailed logging
        if not settings_obj:
            logger.info("=== CREATING NEW SETTINGS RECORD ===")
            settings_obj = InvoiceSettings(
                default_invoice_group=default_invoice_group or "invoice-default",
                default_invoice_terms=default_terms or "Payment due within 30 days",
                invoice_default_payment_method=default_payment_method or "bank_transfer",
                invoices_due_after=invoices_due_after or 30,
                generate_invoice_number_for_draft=generate_invoice_number_draft == "on",
                einvoicing=mark_invoices_sent_pdf == "on",
                pdf_template=default_pdf_template or "default",
                invoice_pdf_password=invoice_pdf_password,
                enable_pdf_watermarks=enable_pdf_watermarks == "on",
                include_zugferd=include_zugferd == "on",
                pdf_invoice_footer=pdf_invoice_footer
            )
            db.add(settings_obj)
            logger.info("New settings object created and added to session")
        else:
            logger.info("=== UPDATING EXISTING SETTINGS RECORD ===")
            settings_obj.default_invoice_group = default_invoice_group or "invoice-default"
            settings_obj.default_invoice_terms = default_terms or "Payment due within 30 days"
            settings_obj.invoice_default_payment_method = default_payment_method or "bank_transfer"
            settings_obj.invoices_due_after = invoices_due_after or 30
            settings_obj.generate_invoice_number_for_draft = generate_invoice_number_draft == "on"
            settings_obj.einvoicing = mark_invoices_sent_pdf == "on"
            settings_obj.pdf_template = default_pdf_template or "default"
            settings_obj.invoice_pdf_password = invoice_pdf_password
            settings_obj.enable_pdf_watermarks = enable_pdf_watermarks == "on"
            settings_obj.include_zugferd = include_zugferd == "on"
            settings_obj.pdf_invoice_footer = pdf_invoice_footer
            logger.info("Existing settings object updated")

        # Step 5: Commit with detailed monitoring
        logger.info("=== COMMITTING CHANGES TO DATABASE ===")
        try:
            db.commit()
            logger.info("✓ Database commit successful")
        except Exception as commit_error:
            logger.error(f"✗ Database commit failed: {commit_error}")
            raise
        
        # Step 6: Refresh with monitoring
        logger.info("=== REFRESHING SETTINGS OBJECT ===")
        try:
            db.refresh(settings_obj)
            logger.info("✓ Settings object refresh successful")
            logger.info(f"Refreshed object ID: {settings_obj.id}")
        except Exception as refresh_error:
            logger.error(f"✗ Settings object refresh failed: {refresh_error}")
            raise
        
        # Step 7: Validate object state before template
        logger.info("=== VALIDATING OBJECT STATE ===")
        try:
            # Test if object attributes are accessible
            test_attrs = [
                'id', 'default_invoice_group', 'default_invoice_terms', 
                'invoice_default_payment_method', 'invoices_due_after',
                'generate_invoice_number_for_draft', 'einvoicing', 
                'pdf_template', 'pdf_invoice_footer'
            ]
            
            for attr in test_attrs:
                try:
                    value = getattr(settings_obj, attr, 'MISSING')
                    logger.info(f"✓ Attribute {attr}: {repr(value)}")
                except Exception as attr_error:
                    logger.error(f"✗ Error accessing attribute {attr}: {attr_error}")
                    
            # Test JSON serialization of the object's key attributes
            serialization_test = {
                'id': settings_obj.id,
                'default_invoice_group': settings_obj.default_invoice_group,
                'default_invoice_terms': settings_obj.default_invoice_terms
            }
            json.dumps(serialization_test)
            logger.info("✓ Object attributes are JSON serializable")
            
        except Exception as validation_error:
            logger.error(f"✗ Object validation failed: {validation_error}")
            # Continue anyway to see what happens
        
        # Step 8: Check template file existence
        logger.info("=== TEMPLATE FILE CHECK ===")
        template_path = Path("app/templates/settings/invoice.html")
        if template_path.exists():
            logger.info(f"✓ Template file exists: {template_path}")
            logger.info(f"Template file size: {template_path.stat().st_size} bytes")
        else:
            logger.error(f"✗ Template file missing: {template_path}")
            # List available templates
            templates_dir = Path("app/templates/settings")
            if templates_dir.exists():
                available_templates = list(templates_dir.glob("*.html"))
                logger.info(f"Available templates: {[t.name for t in available_templates]}")
        
        # Step 9: Prepare template context with validation
        logger.info("=== PREPARING TEMPLATE CONTEXT ===")
        try:
            template_context = {
                "request": request,
                "user": current_user,
                "invoice_settings": settings_obj,
                "success_message": "Invoice settings saved successfully.",
                "title": "Invoice Settings"
            }
            
            # Validate each context item
            for key, value in template_context.items():
                logger.info(f"Context '{key}': {type(value).__name__}")
                if key == "invoice_settings":
                    logger.info(f"  invoice_settings.id: {value.id}")
                elif key == "user":
                    logger.info(f"  user.id: {getattr(value, 'id', 'NO_ID')}")
                elif key == "request":
                    logger.info(f"  request.url: {getattr(value, 'url', 'NO_URL')}")
            
            logger.info("✓ Template context prepared successfully")
            
        except Exception as context_error:
            logger.error(f"✗ Template context preparation failed: {context_error}")
            raise
        
        # Step 10: Test template rendering with required context
        logger.info("=== TESTING TEMPLATE WITH REQUIRED CONTEXT ===")
        try:
            # The template requires invoice_settings, so include it in the test
            test_context = {
                "request": request,
                "user": current_user,
                "invoice_settings": settings_obj,  # This is required!
                "title": "Invoice Settings"
            }
            
            # This is just a test - we won't return this
            test_response = templates.TemplateResponse("settings/invoice.html", test_context)
            logger.info("✓ Template context with invoice_settings works")
            
        except Exception as template_test_error:
            logger.error(f"✗ Template test failed: {template_test_error}")
            logger.error(f"Template test error traceback: {traceback.format_exc()}")
            raise
        
        # Step 11: Create the actual response
        logger.info("=== RENDERING FINAL TEMPLATE RESPONSE ===")
        try:
            response = templates.TemplateResponse("settings/invoice.html", template_context)
            logger.info("✓ Template response created successfully")
            logger.info(f"Response type: {type(response).__name__}")
            logger.info("=== INVOICE SETTINGS SAVE COMPLETED SUCCESSFULLY ===")
            return response
            
        except Exception as template_error:
            logger.error(f"✗ Template rendering failed: {template_error}")
            logger.error(f"Template error type: {type(template_error).__name__}")
            logger.error(f"Template error traceback: {traceback.format_exc()}")
            raise
        
    except Exception as e:
        logger.error("=== CRITICAL ERROR IN SAVE_INVOICE_SETTINGS ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Step 12: Attempt rollback with logging
        try:
            logger.info("Attempting database rollback...")
            db.rollback()
            logger.info("✓ Database rollback completed")
        except Exception as rollback_error:
            logger.error(f"✗ Error during rollback: {rollback_error}")
        
        # Step 13: Prepare error response with safe context
        logger.info("=== PREPARING ERROR RESPONSE ===")
        try:
            # Get current settings safely for error display
            safe_settings = None
            try:
                safe_settings = db.query(InvoiceSettings).first()
                logger.info("✓ Retrieved current settings for error display")
            except Exception as settings_retrieval_error:
                logger.error(f"Could not retrieve settings for error display: {settings_retrieval_error}")
                safe_settings = InvoiceSettings(
                    default_invoice_group="invoice-default",
                    default_invoice_terms="Payment due within 30 days",
                    invoice_default_payment_method="bank_transfer",
                    invoices_due_after=30,
                    generate_invoice_number_for_draft=False,
                    einvoicing=False,
                    pdf_invoice_footer="Thank you for your business",
                    pdf_template="default",
                    invoice_logo=None,
                    invoice_pdf_password=None,
                    enable_pdf_watermarks=False,
                    include_zugferd=False
                )
            
            error_context = {
                "request": request,
                "user": current_user,
                "invoice_settings": safe_settings,
                "error_message": f"Failed to save settings: {str(e)}",
                "title": "Invoice Settings"
            }
            
            logger.info("✓ Error context prepared")
            return templates.TemplateResponse("settings/invoice.html", error_context)
            
        except Exception as error_response_error:
            logger.error(f"✗ Failed to create error response: {error_response_error}")
            logger.error(f"Error response traceback: {traceback.format_exc()}")
            
            # Last resort: return a basic HTTP exception
            raise HTTPException(
                status_code=500, 
                detail=f"Internal server error during settings save: {str(e)}"
            )

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

@router.get("/quote-settings", response_class=HTMLResponse)
async def quote_settings(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Show quote settings page (placeholder)"""
    return templates.TemplateResponse("settings/quote_settings.html", {
        "request": request,
        "user": current_user,
        "title": "Quote Settings"
    })

@router.get("/email", response_class=HTMLResponse)
async def email_settings(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Show email settings page (placeholder)"""
    return templates.TemplateResponse("settings/email.html", {
        "request": request,
        "user": current_user,
        "title": "Email Settings"
    })

@router.get("/online-payment", response_class=HTMLResponse)
async def online_payment_settings(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Show online payment settings page (placeholder)"""
    return templates.TemplateResponse("settings/online_payment.html", {
        "request": request,
        "user": current_user,
        "title": "Online Payment Settings"
    })

@router.get("/projects", response_class=HTMLResponse)
async def projects_settings(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Show projects settings page (placeholder)"""
    return templates.TemplateResponse("settings/projects.html", {
        "request": request,
        "user": current_user,
        "title": "Projects Settings"
    })

@router.get("/updates", response_class=HTMLResponse)
async def updates_settings(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Show updates page (placeholder)"""
    return templates.TemplateResponse("settings/updates.html", {
        "request": request,
        "user": current_user,
        "title": "Updates"
    })