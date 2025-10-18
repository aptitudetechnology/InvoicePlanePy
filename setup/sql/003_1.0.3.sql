-- InvoicePlane Python - Add Missing Product Fields
-- Version: 1.0.3
-- Created: 2025-10-18
-- Description: Adds missing optional fields to products table for compatibility with legacy imports

-- Add missing optional fields to products table
ALTER TABLE products ADD COLUMN IF NOT EXISTS provider_name VARCHAR(255);
ALTER TABLE products ADD COLUMN IF NOT EXISTS purchase_price NUMERIC(10,2);
ALTER TABLE products ADD COLUMN IF NOT EXISTS sumex BOOLEAN DEFAULT FALSE;
ALTER TABLE products ADD COLUMN IF NOT EXISTS tariff NUMERIC(10,2);