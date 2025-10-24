-- InvoicePlane Python - Add Discount Fields to Invoices
-- Version: 1.0.2
-- Created: 2025-09-24
-- Description: Adds discount fields to invoices and invoice_items tables for proper quote-to-invoice conversion

-- Add discount fields to invoices table
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS discount_amount NUMERIC(10,2) DEFAULT 0.00;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS discount_percentage NUMERIC(5,2) DEFAULT 0.00;

-- Add discount field to invoice_items table
ALTER TABLE invoice_items ADD COLUMN IF NOT EXISTS discount_amount NUMERIC(10,2) DEFAULT 0.00;

-- Add discount_amount column to quotes table if it doesn't exist (calculated field)
-- This is handled by the model property, but ensure the column exists for consistency
ALTER TABLE quotes ADD COLUMN IF NOT EXISTS discount_amount NUMERIC(10,2) DEFAULT 0.00;

-- Add discount fields to quote_items table if they don't exist
ALTER TABLE quote_items ADD COLUMN IF NOT EXISTS discount_amount NUMERIC(10,2) DEFAULT 0.00;

-- Create company_settings table for storing company-wide settings
CREATE TABLE IF NOT EXISTS company_settings (
    id SERIAL PRIMARY KEY,
    language VARCHAR(50) DEFAULT 'english',
    theme VARCHAR(100) DEFAULT 'invoiceplane-default',
    first_day_week VARCHAR(20) DEFAULT 'monday',
    date_format VARCHAR(20) DEFAULT 'm/d/Y',
    default_country VARCHAR(10) DEFAULT 'US',
    items_per_page INTEGER DEFAULT 25,
    currency_symbol VARCHAR(10) DEFAULT '$',
    currency_placement VARCHAR(20) DEFAULT 'before',
    currency_code VARCHAR(10) DEFAULT 'USD',
    tax_decimal_places INTEGER DEFAULT 2,
    number_format VARCHAR(20) DEFAULT 'comma_dot',
    company_name VARCHAR(255),
    company_address TEXT,
    company_address_2 TEXT,
    company_city VARCHAR(255),
    company_state VARCHAR(255),
    company_zip VARCHAR(20),
    company_country VARCHAR(10),
    company_phone VARCHAR(50),
    company_email VARCHAR(255),
    default_invoice_tax VARCHAR(50) DEFAULT 'none',
    default_invoice_tax_placement VARCHAR(20) DEFAULT 'after',
    default_item_tax VARCHAR(50) DEFAULT 'none',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default company settings if table is empty
INSERT INTO company_settings DEFAULT VALUES
ON CONFLICT DO NOTHING;

-- Insert default tax rates if table is empty
INSERT INTO tax_rates (name, rate, is_default) VALUES
    ('GST', 10.0, false),
    ('VAT', 20.0, false),
    ('Sales Tax', 8.5, false)
ON CONFLICT (name) DO NOTHING;