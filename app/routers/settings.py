from fastapi import APIRouter, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.invoicesettings import InvoiceSettings
from app.models.company_settings import CompanySettings
from app.models.tax_rate import TaxRate
import logging

# Add this at the top of your file
logger = logging.getLogger(__name__)

from app.routers.products import get_families_api

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Test Product Families API diagnostic endpoint
@router.get("/test-families-api", response_class=JSONResponse)
async def test_families_api(db: Session = Depends(get_db)):
    """
    Test the /products/api/families endpoint and return the result for diagnostics.
    """
    try:
        families_result = await get_families_api(db)
        return {"success": True, "families": families_result.get("families", [])}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Test Products API diagnostic endpoint
@router.get("/test-products-api", response_class=JSONResponse)
async def test_products_api(db: Session = Depends(get_db)):
    """
    Test the /products/api endpoint and return the result for diagnostics.
    """
    try:
        # Import the products API function
        from app.routers.products import get_products_api
        
        # Call the products API with explicit parameters
        products_result = await get_products_api(
            db=db,
            page=1,
            limit=10,
            search=None,
            family_id=None,
            sort_by="name",
            sort_order="asc"
        )
        return {"success": True, "products": products_result.get("products", [])}
    except Exception as e:
        return {"success": False, "error": str(e)}


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
    # Load settings from database or create default if none exist
    company_settings = db.query(CompanySettings).first()
    if not company_settings:
        company_settings = CompanySettings()
        db.add(company_settings)
        db.commit()
        db.refresh(company_settings)
    
    # Load tax rates for the dropdown
    tax_rates = db.query(TaxRate).all()
    
    # Debug: Print what we're passing
    print(f"DEBUG: Loading company settings, found {len(tax_rates)} tax rates")
    for tr in tax_rates:
        print(f"  Tax rate: {tr.name} ({tr.rate}%)")
    
    # Convert settings to dict for template
    settings = {
        "language": company_settings.language,
        "theme": company_settings.theme,
        "first_day_week": company_settings.first_day_week,
        "date_format": company_settings.date_format,
        "default_country": company_settings.default_country,
        "items_per_page": str(company_settings.items_per_page),
        "currency_symbol": company_settings.currency_symbol,
        "currency_placement": company_settings.currency_placement,
        "currency_code": company_settings.currency_code,
        "tax_decimal_places": str(company_settings.tax_decimal_places),
        "number_format": company_settings.number_format,
        "company_name": company_settings.company_name or "",
        "company_address": company_settings.company_address or "",
        "company_address_2": company_settings.company_address_2 or "",
        "company_city": company_settings.company_city or "",
        "company_state": company_settings.company_state or "",
        "company_zip": company_settings.company_zip or "",
        "company_country": company_settings.company_country or "",
        "company_phone": company_settings.company_phone or "",
        "company_email": company_settings.company_email or "",
        "default_invoice_tax": company_settings.default_invoice_tax,
        "default_invoice_tax_placement": company_settings.default_invoice_tax_placement,
        "default_item_tax": company_settings.default_item_tax,
    }
    
    return templates.TemplateResponse("settings/company.html", {
        "request": request,
        "user": current_user,
        "settings": settings,
        "tax_rates": tax_rates,
        "title": "Company Settings"
    })

@router.post("/company", response_class=HTMLResponse)
async def company_settings_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    language: str = Form(None),
    theme: str = Form(None),
    first_day_week: str = Form(None),
    date_format: str = Form(None),
    default_country: str = Form(None),
    items_per_page: str = Form(None),
    currency_symbol: str = Form(None),
    currency_placement: str = Form(None),
    currency_code: str = Form(None),
    tax_decimal_places: str = Form(None),
    number_format: str = Form(None),
    company_name: str = Form(None),
    company_address: str = Form(None),
    company_address_2: str = Form(None),
    company_city: str = Form(None),
    company_state: str = Form(None),
    company_zip: str = Form(None),
    company_country: str = Form(None),
    company_phone: str = Form(None),
    company_email: str = Form(None),
    default_invoice_tax: str = Form(None),
    default_invoice_tax_placement: str = Form(None),
    default_item_tax: str = Form(None),
):
    """Handle company settings form submission"""
    try:
        # Load or create company settings
        company_settings = db.query(CompanySettings).first()
        if not company_settings:
            company_settings = CompanySettings()
            db.add(company_settings)
        
        # Update settings from form data
        company_settings.language = language or "english"
        company_settings.theme = theme or "invoiceplane-default"
        company_settings.first_day_week = first_day_week or "monday"
        company_settings.date_format = date_format or "m/d/Y"
        company_settings.default_country = default_country or "US"
        company_settings.items_per_page = int(items_per_page) if items_per_page else 25
        company_settings.currency_symbol = currency_symbol or "$"
        company_settings.currency_placement = currency_placement or "before"
        company_settings.currency_code = currency_code or "USD"
        company_settings.tax_decimal_places = int(tax_decimal_places) if tax_decimal_places else 2
        company_settings.number_format = number_format or "comma_dot"
        company_settings.company_name = company_name
        company_settings.company_address = company_address
        company_settings.company_address_2 = company_address_2
        company_settings.company_city = company_city
        company_settings.company_state = company_state
        company_settings.company_zip = company_zip
        company_settings.company_country = company_country
        company_settings.company_phone = company_phone
        company_settings.company_email = company_email
        company_settings.default_invoice_tax = default_invoice_tax or "none"
        company_settings.default_invoice_tax_placement = default_invoice_tax_placement or "after"
        company_settings.default_item_tax = default_item_tax or "none"
        
        db.commit()
        db.refresh(company_settings)
        
        logger.info(f"Company settings updated by user {current_user.id}")
        
        # Load tax rates for the template
        tax_rates = db.query(TaxRate).all()
        
        # Convert settings back to dict for template
        settings = {
            "language": company_settings.language,
            "theme": company_settings.theme,
            "first_day_week": company_settings.first_day_week,
            "date_format": company_settings.date_format,
            "default_country": company_settings.default_country,
            "items_per_page": str(company_settings.items_per_page),
            "currency_symbol": company_settings.currency_symbol,
            "currency_placement": company_settings.currency_placement,
            "currency_code": company_settings.currency_code,
            "tax_decimal_places": str(company_settings.tax_decimal_places),
            "number_format": company_settings.number_format,
            "company_name": company_settings.company_name or "",
            "company_address": company_settings.company_address or "",
            "company_address_2": company_settings.company_address_2 or "",
            "company_city": company_settings.company_city or "",
            "company_state": company_settings.company_state or "",
            "company_zip": company_settings.company_zip or "",
            "company_country": company_settings.company_country or "",
            "company_phone": company_settings.company_phone or "",
            "company_email": company_settings.company_email or "",
            "default_invoice_tax": company_settings.default_invoice_tax,
            "default_invoice_tax_placement": company_settings.default_invoice_tax_placement,
            "default_item_tax": company_settings.default_item_tax,
        }
        
        return templates.TemplateResponse("settings/company.html", {
            "request": request,
            "user": current_user,
            "settings": settings,
            "tax_rates": tax_rates,
            "success_message": "Company settings saved successfully!",
            "title": "Company Settings"
        })
        
    except Exception as e:
        logger.error(f"Error saving company settings: {str(e)}")
        db.rollback()
        
        # Load tax rates for error template
        tax_rates = db.query(TaxRate).all()
        
        # Return with error - use submitted values
        settings = {
            "language": language or "english",
            "theme": theme or "invoiceplane-default",
            "first_day_week": first_day_week or "monday",
            "date_format": date_format or "m/d/Y",
            "default_country": default_country or "US",
            "items_per_page": items_per_page or "25",
            "currency_symbol": currency_symbol or "$",
            "currency_placement": currency_placement or "before",
            "currency_code": currency_code or "USD",
            "tax_decimal_places": tax_decimal_places or "2",
            "number_format": number_format or "comma_dot",
            "company_name": company_name or "",
            "company_address": company_address or "",
            "company_address_2": company_address_2 or "",
            "company_city": company_city or "",
            "company_state": company_state or "",
            "company_zip": company_zip or "",
            "company_country": company_country or "",
            "company_phone": company_phone or "",
            "company_email": company_email or "",
            "default_invoice_tax": default_invoice_tax or "none",
            "default_invoice_tax_placement": default_invoice_tax_placement or "after",
            "default_item_tax": default_item_tax or "none",
        }
        
        return templates.TemplateResponse("settings/company.html", {
            "request": request,
            "user": current_user,
            "settings": settings,
            "tax_rates": tax_rates,
            "error_message": f"Error saving settings: {str(e)}",
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
        
        # Step 10: Test minimal template rendering first
        logger.info("=== TESTING MINIMAL TEMPLATE CONTEXT ===")
        try:
            minimal_context = {
                "request": request,
                "user": current_user,
                "title": "Invoice Settings"
            }
            
            # Provide the required context for safe test rendering
            minimal_context["invoice_settings"] = settings_obj
            #test_response = templates.TemplateResponse("settings/invoice.html", minimal_context)

            
        except Exception as minimal_error:
            logger.error(f"✗ Even minimal template context fails: {minimal_error}")
            logger.error(f"Minimal error traceback: {traceback.format_exc()}")
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

# Experimental SQL Import routes
@router.post("/import/clients-sql")
async def import_clients_sql(
    request: Request,
    sql_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Import clients from SQL file"""
    try:
        # Save uploaded file temporarily
        import tempfile
        import os
        from pathlib import Path

        with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as temp_file:
            content = await sql_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Import clients using the legacy importer
        from importdb.import_legacy_data import import_clients

        # Run import (not dry run)
        import_clients(dry_run=False, sql_file=temp_file_path)

        # Clean up temp file
        os.unlink(temp_file_path)

        return JSONResponse({
            "success": True,
            "message": "Clients imported successfully from SQL file"
        })

    except Exception as e:
        logger.error(f"Error importing clients from SQL: {e}")
        return JSONResponse({
            "success": False,
            "message": f"Import failed: {str(e)}"
        }, status_code=500)

@router.post("/import/products-sql")
async def import_products_sql(
    request: Request,
    sql_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Import products from SQL file"""
    try:
        # Save uploaded file temporarily
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as temp_file:
            content = await sql_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Import families first, then products using the legacy importer
        from importdb.import_legacy_data import import_families, import_products

        # Import families first
        family_id_mapping = import_families(dry_run=False, sql_file=temp_file_path)

        # Run product import with family mapping
        import_products(dry_run=False, sql_file=temp_file_path, family_id_mapping=family_id_mapping)

        # Clean up temp file
        os.unlink(temp_file_path)

        return JSONResponse({
            "success": True,
            "message": "Products imported successfully from SQL file"
        })

    except Exception as e:
        logger.error(f"Error importing products from SQL: {e}")
        return JSONResponse({
            "success": False,
            "message": f"Import failed: {str(e)}"
        }, status_code=500)

@router.post("/diagnostic")
async def run_import_diagnostic(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run import diagnostic and return results"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    try:
        # Import the diagnostic functions
        import sys
        import os
        sys.path.append('/app')

        from app.config import settings
        from sqlalchemy import create_engine
        from importdb.diagnostic import check_database_content, run_verification, test_sql_parsing
        import io
        from contextlib import redirect_stdout, redirect_stderr

        # Create database engine directly (not using FastAPI dependency)
        engine = create_engine(settings.DATABASE_URL)

        # Capture output
        output_buffer = io.StringIO()

        with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
            print("🔍 InvoicePlane Import Diagnostic Tool")
            print("="*50)

            try:
                test_sql_parsing()
                check_database_content()
                run_verification()

                print("\n" + "="*50)
                print("✅ DIAGNOSTIC COMPLETE")
                print("="*50)

            except Exception as e:
                print(f"\n❌ DIAGNOSTIC FAILED: {e}")
                import traceback
                traceback.print_exc()

        output = output_buffer.getvalue()

        return JSONResponse({
            "success": True,
            "output": output
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.post("/import/invoices-sql")
async def import_invoices_sql(
    request: Request,
    sql_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Import invoices from SQL file"""
    try:
        # Save uploaded file temporarily
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as temp_file:
            content = await sql_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        logger.info(f"Uploaded SQL file saved to: {temp_file_path}")

        # Import invoices using the legacy importer
        try:
            from importdb.import_legacy_data import import_invoices
            logger.info("Successfully imported import_invoices function")
        except Exception as e:
            logger.error(f"Failed to import import_invoices: {e}")
            raise

        # Run import (not dry run)
        logger.info("Starting invoice import...")
        import_invoices(dry_run=False, sql_file=temp_file_path)

        # Clean up temp file
        os.unlink(temp_file_path)

        return JSONResponse({
            "success": True,
            "message": "Invoices imported successfully from SQL file"
        })

    except Exception as e:
        logger.error(f"Error importing invoices from SQL: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JSONResponse({
            "success": False,
            "message": f"Import failed: {type(e).__name__}: {str(e) or 'No message'}"
        }, status_code=500)

@router.post("/import/complete-sql")
async def import_complete_sql(
    request: Request,
    sql_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Import all data in correct order: Products → Clients → Invoices"""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as temp_file:
        content = await sql_file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    logger.info(f"Starting complete SQL import from file: {temp_file_path}")

    results = {
        "families": {"success": False, "message": "", "count": 0},
        "tax_rates": {"success": False, "message": "", "count": 0},
        "products": {"success": False, "message": "", "count": 0},
        "clients": {"success": False, "message": "", "count": 0},
        "invoices": {"success": False, "message": "", "count": 0}
    }

    try:
        # 1. Import Product Families First
        logger.info("Step 1: Importing product families...")
        family_id_mapping = {}
        try:
            from importdb.import_legacy_data import import_families
            family_id_mapping = import_families(dry_run=False, sql_file=temp_file_path)
            # Count families after import
            from app.models.product import ProductFamily
            results["families"]["count"] = db.query(ProductFamily).count()
            results["families"]["success"] = True
            results["families"]["message"] = f"Successfully imported {results['families']['count']} product families"
            logger.info(f"Families import completed: {results['families']['count']} families, {len(family_id_mapping)} ID mappings")
        except Exception as e:
            logger.error(f"Families import failed: {e}")
            results["families"]["message"] = f"Families import failed: {str(e)}"
            # Families are optional, continue with tax rates

        # 2. Import Tax Rates Second
        logger.info("Step 2: Importing tax rates...")
        tax_rate_id_mapping = {}
        try:
            from importdb.import_legacy_data import import_tax_rates
            tax_rate_id_mapping = import_tax_rates(dry_run=False, sql_file=temp_file_path)
            # Count tax rates after import
            from app.models.tax_rate import TaxRate
            results["tax_rates"]["count"] = db.query(TaxRate).count()
            results["tax_rates"]["success"] = True
            results["tax_rates"]["message"] = f"Successfully imported {results['tax_rates']['count']} tax rates"
            logger.info(f"Tax rates import completed: {results['tax_rates']['count']} tax rates, {len(tax_rate_id_mapping)} ID mappings")
        except Exception as e:
            logger.error(f"Tax rates import failed: {e}")
            results["tax_rates"]["message"] = f"Tax rates import failed: {str(e)}"
            # Tax rates are required for products, stop if they fail
            raise

        # 3. Import Products Third
        logger.info("Step 3: Importing products...")
        try:
            from importdb.import_legacy_data import import_products
            product_id_mapping = import_products(dry_run=False, sql_file=temp_file_path, family_id_mapping=family_id_mapping)
            # Count products after import
            from app.models.product import Product
            results["products"]["count"] = db.query(Product).count()
            results["products"]["success"] = True
            results["products"]["message"] = f"Successfully imported {results['products']['count']} products"
            logger.info(f"Products import completed: {results['products']['count']} products, {len(product_id_mapping)} ID mappings")
        except Exception as e:
            logger.error(f"Products import failed: {e}")
            results["products"]["message"] = f"Products import failed: {str(e)}"
            raise  # Stop the process if products fail

        # 4. Import Clients Fourth
        logger.info("Step 4: Importing clients...")
        try:
            from importdb.import_legacy_data import import_clients
            client_id_mapping = import_clients(dry_run=False, sql_file=temp_file_path)
            # Count clients after import
            from app.models.client import Client
            results["clients"]["count"] = db.query(Client).count()
            results["clients"]["success"] = True
            results["clients"]["message"] = f"Successfully imported {results['clients']['count']} clients"
            logger.info(f"Clients import completed: {results['clients']['count']} clients, {len(client_id_mapping)} ID mappings")
        except Exception as e:
            logger.error(f"Clients import failed: {e}")
            results["clients"]["message"] = f"Clients import failed: {str(e)}"
            raise  # Stop the process if clients fail

        # 5. Import Invoices Last
        logger.info("Step 5: Importing invoices...")
        logger.info(f"Client ID mapping has {len(client_id_mapping)} entries")
        logger.info(f"Product ID mapping has {len(product_id_mapping)} entries")
        try:
            from importdb.import_legacy_data import import_invoices
            import_invoices(dry_run=False, sql_file=temp_file_path, client_id_mapping=client_id_mapping, product_id_mapping=product_id_mapping)
            # Count invoices after import
            from app.models.invoice import Invoice, InvoiceItem
            invoice_count = db.query(Invoice).count()
            item_count = db.query(InvoiceItem).count()
            results["invoices"]["count"] = invoice_count
            results["invoices"]["success"] = True
            results["invoices"]["message"] = f"Successfully imported {invoice_count} invoices with {item_count} items"
            logger.info(f"Invoices import completed: {invoice_count} invoices, {item_count} items")
        except Exception as e:
            logger.error(f"Invoices import failed: {e}")
            results["invoices"]["message"] = f"Invoices import failed: {str(e)}"
            raise

        # Clean up temp file
        os.unlink(temp_file_path)

        # All imports successful
        success_message = f"Complete import successful! Imported {results['families']['count']} product families, {results['tax_rates']['count']} tax rates, {results['products']['count']} products, {results['clients']['count']} clients, and {results['invoices']['count']} invoices with {item_count} invoice items."

        return JSONResponse({
            "success": True,
            "message": success_message,
            "results": results
        })

    except Exception as e:
        # Clean up temp file
        try:
            os.unlink(temp_file_path)
        except:
            pass

        logger.error(f"Complete import failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")

        error_message = f"Complete import failed during {next((k for k, v in results.items() if not v['success']), 'unknown')} import: {str(e)}"

        return JSONResponse({
            "success": False,
            "message": error_message,
            "results": results
        }, status_code=500)

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

@router.post("/api/keys/{key_id}/regenerate")
async def regenerate_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Regenerate an existing API key"""
    import secrets
    import hashlib

    # Find the existing key
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    # Generate a new secure random key
    raw_key = f"sk_{secrets.token_urlsafe(32)}"

    # Hash the new key
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    # Update the existing record
    api_key.key_hash = key_hash
    api_key.key_prefix = raw_key[:8]
    api_key.last_used_at = None  # Reset last used time

    db.commit()

    return JSONResponse({
        "success": True,
        "key": raw_key,
        "message": "API key regenerated successfully"
    })

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