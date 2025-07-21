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
            db.execute("SELECT 1")
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
            
            # This is just a test - we won't return this
            test_response = templates.TemplateResponse("settings/invoice.html", minimal_context)
            logger.info("✓ Minimal template context works")
            
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