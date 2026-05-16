sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================
-- USERS
-- =========================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,

    role VARCHAR(50) NOT NULL DEFAULT 'employee',

    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================
-- PRODUCTS
-- =========================

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,
    description TEXT,

    price NUMERIC(10,2) NOT NULL,

    stock INTEGER DEFAULT 0,

    is_available BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================
-- ORDERS
-- =========================

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    customer_name VARCHAR(255),
    customer_phone VARCHAR(50),

    delivery_address TEXT,

    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',

    total_price NUMERIC(10,2) DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================
-- ORDER ITEMS
-- =========================

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID NOT NULL,
    product_id UUID NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_order
        FOREIGN KEY(order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_product
        FOREIGN KEY(product_id)
        REFERENCES products(id)
);

