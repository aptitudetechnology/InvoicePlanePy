-- InvoicePlane Python - Add Quote to Invoice Support
-- Version: 1.0.1
-- Created: 2025-09-23
-- Description: Adds invoice_id column to quotes table for tracking conversions

-- Add invoice_id column to quotes table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'quotes' AND column_name = 'invoice_id'
    ) THEN
        ALTER TABLE quotes ADD COLUMN invoice_id INTEGER REFERENCES invoices(id);
        RAISE NOTICE 'Added invoice_id column to quotes table';
    ELSE
        RAISE NOTICE 'invoice_id column already exists in quotes table';
    END IF;
END $$;

-- Add discount_percentage column to quotes table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'quotes' AND column_name = 'discount_percentage'
    ) THEN
        ALTER TABLE quotes ADD COLUMN discount_percentage NUMERIC(5,2) DEFAULT 0.00;
        RAISE NOTICE 'Added discount_percentage column to quotes table';
    ELSE
        RAISE NOTICE 'discount_percentage column already exists in quotes table';
    END IF;
END $$;

-- Ensure all required quote statuses exist
INSERT INTO quote_statuses (name, description, is_active)
VALUES
    ('DRAFT', 'Quote is being drafted. Not yet sent to the client.', true),
    ('SENT', 'Quote has been sent to the client.', true),
    ('VIEWED', 'Client has viewed the quote.', true),
    ('ACCEPTED', 'Client has accepted the quote.', true),
    ('REJECTED', 'Client has rejected the quote.', true),
    ('EXPIRED', 'Quote has expired.', true),
    ('CONVERTED', 'Quote has been converted to an invoice.', true)
ON CONFLICT (name) DO NOTHING;