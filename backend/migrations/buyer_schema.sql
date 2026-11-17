-- ====================================================================
-- AgriMate AI - Buyer Dashboard PostgreSQL Schema
-- Tables:
-- 1. buyer_preferences
-- 2. listings
-- 3. interests
-- 4. deal_status_history
-- 5. notifications
-- ====================================================================

-- 1. Buyer Preferences
CREATE TABLE IF NOT EXISTS buyer_preferences (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    preferred_crops TEXT NOT NULL DEFAULT 'Potato,Tomato',
    preferred_grade VARCHAR(10) NOT NULL DEFAULT 'A',
    min_qty REAL NOT NULL DEFAULT 1000.0,
    max_qty REAL NOT NULL DEFAULT 10000.0,
    latitude REAL DEFAULT 31.5204,
    longitude REAL DEFAULT 74.3587,
    location VARCHAR(150) NOT NULL DEFAULT 'Lahore Badami Bagh Mandi',
    max_budget_price REAL NOT NULL DEFAULT 2600.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_buyer_pref_buyer_id ON buyer_preferences(buyer_id);

-- 2. Farmer Produce Listings
CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    farmer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    crop VARCHAR(80) NOT NULL,
    grade VARCHAR(10) NOT NULL DEFAULT 'A',
    quantity REAL NOT NULL,
    asking_price REAL NOT NULL,
    latitude REAL,
    longitude REAL,
    location VARCHAR(150) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT check_listing_grade CHECK (grade IN ('A', 'B', 'C')),
    CONSTRAINT check_listing_status CHECK (status IN ('active', 'deal_pending', 'sold', 'cancelled'))
);

CREATE INDEX IF NOT EXISTS idx_listings_crop ON listings(crop);
CREATE INDEX IF NOT EXISTS idx_listings_grade ON listings(grade);
CREATE INDEX IF NOT EXISTS idx_listings_status ON listings(status);
CREATE INDEX IF NOT EXISTS idx_listings_farmer ON listings(farmer_id);

-- 3. Buyer Purchase Interests (Deals)
CREATE TABLE IF NOT EXISTS interests (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    buyer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT,
    offered_price REAL NOT NULL,
    quantity_wanted REAL NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'interested',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT check_interest_status CHECK (status IN ('interested', 'accepted', 'in_progress', 'completed', 'rejected'))
);

CREATE INDEX IF NOT EXISTS idx_interests_listing ON interests(listing_id);
CREATE INDEX IF NOT EXISTS idx_interests_buyer ON interests(buyer_id);
CREATE INDEX IF NOT EXISTS idx_interests_status ON interests(status);

-- 4. Deal Status History (Audit Timeline)
CREATE TABLE IF NOT EXISTS deal_status_history (
    id SERIAL PRIMARY KEY,
    interest_id INTEGER NOT NULL REFERENCES interests(id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL,
    notes TEXT,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_deal_history_interest ON deal_status_history(interest_id);

-- 5. Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL DEFAULT 'SYSTEM',
    title VARCHAR(150) NOT NULL,
    title_ur VARCHAR(200),
    message TEXT NOT NULL,
    message_ur TEXT,
    data_json TEXT,
    fcm_message_id VARCHAR(100),
    fcm_dispatched BOOLEAN DEFAULT FALSE NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
