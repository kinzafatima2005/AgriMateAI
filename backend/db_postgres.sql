-- ====================================================================
-- AgriMate AI - PostgreSQL Production Schema
-- Compatible with PostgreSQL 13, 14, 15, 16+
-- ====================================================================

-- 1. Create User Roles Enum (or use VARCHAR with CHECK)
CREATE TYPE user_role_enum AS ENUM ('Farmer', 'Buyer', 'Expert/Admin');

-- 2. Users Table (Strict Minimal Registration Schema)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    phone_or_email VARCHAR(120) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'Farmer',
    location VARCHAR(150) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT check_user_role CHECK (role IN ('Farmer', 'Buyer', 'Expert/Admin'))
);

CREATE INDEX IF NOT EXISTS idx_users_phone_or_email ON users(phone_or_email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_location ON users(location);

-- 3. Crop Diary Entries (Offline-First Syncing with Client UUID)
CREATE TABLE IF NOT EXISTS crop_diary_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_uuid VARCHAR(64) UNIQUE NOT NULL,
    crop_name VARCHAR(80) NOT NULL,
    variety VARCHAR(80),
    field_name VARCHAR(100),
    acreage REAL NOT NULL DEFAULT 1.0,
    activity_type VARCHAR(50) NOT NULL,
    activity_date TIMESTAMP WITH TIME ZONE NOT NULL,
    details TEXT,
    cost_pkr REAL NOT NULL DEFAULT 0.0,
    client_updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    server_synced_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_crop_diary_user_id ON crop_diary_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_crop_diary_client_uuid ON crop_diary_entries(client_uuid);

-- 4. Leaf Disease Scans & Grad-CAM Heatmaps
CREATE TABLE IF NOT EXISTS disease_scans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop_name VARCHAR(80) NOT NULL,
    predicted_disease VARCHAR(120) NOT NULL,
    confidence REAL NOT NULL,
    severity_level VARCHAR(30) NOT NULL,
    image_url VARCHAR(255),
    gradcam_heatmap_url VARCHAR(255),
    treatment_protocol_json TEXT,
    citation_source VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_disease_scans_user_id ON disease_scans(user_id);

-- 5. Marketplace: Crop Listings (Farmers)
CREATE TABLE IF NOT EXISTS crop_listings (
    id SERIAL PRIMARY KEY,
    farmer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop_name VARCHAR(80) NOT NULL,
    variety VARCHAR(80),
    grade VARCHAR(10) NOT NULL DEFAULT 'A',
    quantity_kg REAL NOT NULL,
    price_per_maund_pkr REAL NOT NULL,
    district VARCHAR(80) NOT NULL,
    province VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'AVAILABLE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_crop_listings_district ON crop_listings(district);
CREATE INDEX IF NOT EXISTS idx_crop_listings_status ON crop_listings(status);

-- 6. Marketplace: Buyer Demands
CREATE TABLE IF NOT EXISTS buyer_demands (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop_name VARCHAR(80) NOT NULL,
    variety_preference VARCHAR(80),
    min_grade VARCHAR(10) NOT NULL DEFAULT 'B',
    required_quantity_kg REAL NOT NULL,
    max_price_per_maund_pkr REAL NOT NULL,
    target_district VARCHAR(80),
    target_province VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 7. Seed Demo Users in PostgreSQL
INSERT INTO users (name, phone_or_email, hashed_password, role, location, is_active)
VALUES 
    (
        'Muhammad Tariq (Cotton & Wheat Farmer)', 
        '03001234567', 
        'pbkdf2_sha256$600000$87d90e668ff46d84a7536965be2fbb14$63c87f4c5e31a29b0151167e4e0bfaab03f90117ea5cf83d57d5427aa21a97e6', 
        'Farmer', 
        'Multan, Punjab', 
        TRUE
    ),
    (
        'Haji Abdul Rehman (Grain Mandi Buyer)', 
        '03219876543', 
        'pbkdf2_sha256$600000$87d90e668ff46d84a7536965be2fbb14$63c87f4c5e31a29b0151167e4e0bfaab03f90117ea5cf83d57d5427aa21a97e6', 
        'Buyer', 
        'Faisalabad, Punjab', 
        TRUE
    ),
    (
        'Dr. Farooq Shah (Agronomy Expert)', 
        'expert.farooq@agrimate.pk', 
        'pbkdf2_sha256$600000$87d90e668ff46d84a7536965be2fbb14$63c87f4c5e31a29b0151167e4e0bfaab03f90117ea5cf83d57d5427aa21a97e6', 
        'Expert/Admin', 
        'Lahore, Punjab', 
        TRUE
    )
ON CONFLICT (phone_or_email) DO NOTHING;

