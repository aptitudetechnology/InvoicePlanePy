# Plan to Persist Invoice Settings in InvoicePlanePy

## 1. Files to Edit

- `app/routers/settings.py` (add database save logic to the POST handler for invoice settings)
- `app/models/invoicesettings.py` (ensure model matches schema and supports updates)
- `app/templates/settings/invoice.html` (optional: update success message after persistence)

## 2. Steps and Code Required

### Step 1: Update the POST Route in `settings.py`

Replace the placeholder logic in the POST `/invoices` handler with code to save/update settings in the database:

```python
from app.models.invoicesettings import InvoiceSettings

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
):
    settings = {
        "default_invoice_group": default_invoice_group,
        "default_invoice_terms": default_terms,
        "invoice_default_payment_method": default_payment_method,
        "invoices_due_after": invoices_due_after,
        "generate_invoice_number_for_draft": generate_invoice_number_draft == "true",
        "enable_pdf_watermarks": enable_pdf_watermarks == "true",
        "invoice_pdf_password": invoice_pdf_password,
        "include_zugferd": include_zugferd == "true",
        "pdf_template": default_pdf_template
    }
    # Save or update settings in DB
    settings_obj = db.query(InvoiceSettings).first()
    if not settings_obj:
        settings_obj = InvoiceSettings(**settings)
        db.add(settings_obj)
    else:
        for key, value in settings.items():
            setattr(settings_obj, key, value)
    db.commit()
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "invoice_settings": settings_obj,
        "success_message": "Settings saved successfully."
    })
```

### Step 2: Ensure Model Supports All Fields

Check `app/models/invoicesettings.py` for all required fields and types. Update if needed to match the form and schema.

### Step 3: Update Success Message (Optional)

In `app/templates/settings/invoice.html`, update the success message to confirm persistence:

```html
{% if success_message %}
<div class="alert alert-success alert-dismissible fade show" role="alert">
    {{ success_message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endif %}
```

## 3. Testing

- Submit the form and verify that settings are saved in the `invoice_settings` table.
- Reload the page and confirm settings are loaded from the database.

## Implementation Checklist

- [ ] Update `app/routers/settings.py` to persist invoice settings in the database
- [ ] Ensure all required fields are present in `app/models/invoicesettings.py`
- [ ] Confirm form field names in `app/templates/settings/invoice.html` match backend keys
- [ ] Update success message in `app/templates/settings/invoice.html` to confirm persistence
- [ ] Test form submission and verify data is saved in `invoice_settings` table
- [ ] Test loading and displaying settings from the database
- [ ] Remove any remaining TODO comments related to invoice settings persistence
- [ ] Document any additional changes or edge cases

---

**Summary:**
- Edit `settings.py` to persist settings.
- Ensure model and template support all fields.
- Test saving and loading functionality.
