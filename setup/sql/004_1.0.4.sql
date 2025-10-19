-- InvoicePlane Python - Add API Key Prefix Column
-- Version: 1.0.4
-- Created: 2025-10-19
-- Description: Adds the missing key_prefix column to the api_keys table

-- Add key_prefix column to api_keys table if it doesn't exist
ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS key_prefix VARCHAR(10) NOT NULL DEFAULT 'sk-';