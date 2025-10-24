invoicesettings_schema = {
    "id": {
        "type": "integer",
        "primary_key": True,
        "description": "Primary key for invoice settings"
    },
    "default_invoice_group": {
        "type": "string",
        "max_length": 50,
        "description": "Default invoice group ID or name"
    },
    "default_invoice_terms": {
        "type": "text",
        "description": "Default terms for invoices"
    },
    "invoice_default_payment_method": {
        "type": "string",
        "max_length": 50,
        "description": "Default payment method for invoices"
    },
    "invoices_due_after": {
        "type": "integer",
        "description": "Number of days after issue date that invoices are due"
    },
    "generate_invoice_number_for_draft": {
        "type": "boolean",
        "description": "Whether to generate invoice number for draft invoices"
    },
    "einvoicing": {
        "type": "boolean",
        "description": "Enable e-invoicing features"
    },
    "pdf_invoice_footer": {
        "type": "text",
        "description": "Footer text for invoice PDFs"
    },
    "pdf_template": {
        "type": "string",
        "max_length": 100,
        "description": "Default PDF template for invoices"
    },
    "invoice_logo": {
        "type": "string",
        "max_length": 255,
        "description": "Logo file name or path for invoices"
    },
    "invoice_pdf_password": {
        "type": "string",
        "max_length": 255,
        "description": "Password for invoice PDF files"
    },
    "enable_pdf_watermarks": {
        "type": "boolean",
        "description": "Enable watermarks on invoice PDFs"
    },
    "include_zugferd": {
        "type": "boolean",
        "description": "Include Zugferd XML in invoice PDFs"
    },
    "created_at": {
        "type": "timestamp",
        "description": "Record creation timestamp"
    },
    "updated_at": {
        "type": "timestamp",
        "description": "Record last update timestamp"
    }
}
