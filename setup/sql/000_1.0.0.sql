-- InvoicePlane Python - Initial Database Schema
-- Version: 1.0.0
-- Created: 2025-01-07

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    company VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Corrected Clients table - matches SQLAlchemy Client model
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    
    -- Personal Information
    is_active BOOLEAN DEFAULT true,
    name VARCHAR(100) NOT NULL,        -- Changed from 255 to 100 to match model
    surname VARCHAR(100),              -- Changed from 255 to 100 to match model
    language VARCHAR(10) DEFAULT 'en',
    
    -- Address
    address_1 VARCHAR(255),
    address_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(50),               -- Changed from 100 to 50 to match model
    
    -- Contact Information
    phone VARCHAR(20),
    fax VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),              -- Added (was 'web' before)
    
    -- Personal Information (Additional)
    gender VARCHAR(10),                -- Added
    birthdate DATE,                    -- Added
    company VARCHAR(255),              -- Added
    
    -- Taxes Information
    vat_id VARCHAR(50),
    tax_code VARCHAR(50),
    abn VARCHAR(50),                   -- Added (Australian Business Number)
    
    -- Legacy fields for compatibility
    title VARCHAR(50),                 -- Added
    
    -- Notes
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ProductFamily table FIRST
CREATE TABLE IF NOT EXISTS product_families (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ProductUnit table SECOND
CREATE TABLE IF NOT EXISTS product_units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table LAST (after its dependencies exist)
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) DEFAULT 0.00,
    sku VARCHAR(100) UNIQUE NOT NULL,
    tax_rate NUMERIC(5, 2) DEFAULT 0.00,
    family_id INTEGER REFERENCES product_families(id),
    unit_id INTEGER REFERENCES product_units(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS quote_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    client_id INTEGER NOT NULL REFERENCES clients(id),
    quote_number VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(255),
    issue_date DATE NOT NULL,
    valid_until DATE,
--  quote_pdf_password VARCHAR(255),
    total NUMERIC(10,2) NOT NULL,
    balance NUMERIC(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'AUD',
    status INTEGER NOT NULL REFERENCES quote_statuses(id),
    notes TEXT,
    tax_rate NUMERIC(5,2) DEFAULT 0.00,
    tax_amount NUMERIC(10,2),
    subtotal NUMERIC(10,2),
    item_tax_total NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS quote_items (
    id SERIAL PRIMARY KEY,
    quote_id INTEGER NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    product_name VARCHAR(255),
    description TEXT,
    unit_price NUMERIC(10, 2) NOT NULL,
    quantity NUMERIC(10, 2) NOT NULL,
    discount_percentage NUMERIC(5, 2) DEFAULT 0.00,
    tax_rate NUMERIC(5, 2) DEFAULT 0.00,
    tax_amount NUMERIC(10, 2),
    subtotal NUMERIC(10, 2),
    discount_amount NUMERIC(10, 2),
    total NUMERIC(10, 2),
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


-- Invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    client_id INTEGER REFERENCES clients(id) NOT NULL,
    invoice_number VARCHAR(20) UNIQUE NOT NULL,
    status INTEGER DEFAULT 1, -- 1=DRAFT, 2=SENT, 3=VIEWED, 4=PAID, 5=OVERDUE, 6=CANCELLED
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    terms TEXT,
    notes TEXT,
    url_key VARCHAR(32) UNIQUE,
    subtotal NUMERIC(10, 2) DEFAULT 0.00,
    tax_total NUMERIC(10, 2) DEFAULT 0.00,
    total NUMERIC(10, 2) DEFAULT 0.00,
    paid_amount NUMERIC(10, 2) DEFAULT 0.00,
    balance NUMERIC(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) NOT NULL,
    product_id INTEGER REFERENCES products(id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    quantity NUMERIC(10, 2) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    "order" INTEGER DEFAULT 0,
    subtotal NUMERIC(10, 2),
    tax_amount NUMERIC(10, 2),
    total NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Invoice settings table
CREATE TABLE IF NOT EXISTS invoice_settings (
    id SERIAL PRIMARY KEY,
    default_invoice_group VARCHAR(50),
    default_invoice_terms TEXT,
    invoice_default_payment_method VARCHAR(50),
    invoices_due_after INTEGER,
    generate_invoice_number_for_draft BOOLEAN DEFAULT FALSE,
    einvoicing BOOLEAN DEFAULT FALSE,
    pdf_invoice_footer TEXT,
    pdf_template VARCHAR(100),
    invoice_logo VARCHAR(255),
    invoice_pdf_password VARCHAR(255),
    enable_pdf_watermarks BOOLEAN DEFAULT FALSE,
    include_zugferd BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);







-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50),
    reference VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tax Rates table
CREATE TABLE IF NOT EXISTS tax_rate (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    rate NUMERIC(5, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_user ON invoices(user_id);
CREATE INDEX IF NOT EXISTS idx_invoices_client ON invoices(client_id);
CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice ON invoice_items(invoice_id);
CREATE INDEX IF NOT EXISTS idx_payments_invoice ON payments(invoice_id);
CREATE INDEX IF NOT EXISTS idx_quotes_number ON quotes(quote_number);
CREATE INDEX IF NOT EXISTS idx_quotes_user ON quotes(user_id);
CREATE INDEX IF NOT EXISTS idx_quotes_client ON quotes(client_id);
CREATE INDEX IF NOT EXISTS idx_quote_items_quote ON quote_items(quote_id);
CREATE INDEX IF NOT EXISTS idx_quote_items_product ON quote_items(product_id);

