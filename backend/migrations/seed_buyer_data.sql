-- ====================================================================
-- AgriMate AI - Seed Buyer Data (PostgreSQL)
-- 5 Buyers, 20 Listings across Potato/Tomato/Wheat, sample interests
-- ====================================================================

-- 1. Insert Farmers (if not already existing)
INSERT INTO users (phone_or_email, hashed_password, name, role, location, is_active, created_at, updated_at)
VALUES 
    ('03001112233', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Haji Ghulam Rasool', 'Farmer', 'Okara, Punjab', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03002223344', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Chaudhry Akram', 'Farmer', 'Sahiwal, Punjab', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03003334455', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Malik Riaz', 'Farmer', 'Multan, Punjab', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03004445566', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Mian Tariq Farooq', 'Farmer', 'Faisalabad, Punjab', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (phone_or_email) DO UPDATE SET role = EXCLUDED.role;

-- 2. Insert 5 Buyers
INSERT INTO users (phone_or_email, hashed_password, name, role, location, is_active, created_at, updated_at)
VALUES 
    ('03211110001', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Tariq Traders (Lahore Mandi)', 'Buyer', 'Lahore Badami Bagh Mandi', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03211110002', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Al-Rehman Foods (Multan)', 'Buyer', 'Multan Ghalla Mandi', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03211110003', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'National Agro Processors', 'Buyer', 'Faisalabad Sammundri Rd Mandi', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03211110004', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Bismillah Grain House', 'Buyer', 'Sahiwal Grain Market', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('03211110005', '$2b$12$KkQc9L7WJz0f2j0P2z0f2.0123456789abcdefghijklmnopqrstuv', 'Khyber Mandi Wholesalers', 'Buyer', 'Rawalpindi Sabzi Mandi I-11', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (phone_or_email) DO UPDATE SET role = 'Buyer';

-- 3. Buyer Preferences
INSERT INTO buyer_preferences (buyer_id, preferred_crops, preferred_grade, min_qty, max_qty, latitude, longitude, location, max_budget_price, updated_at)
SELECT id, 'Potato,Tomato', 'A', 2000.0, 15000.0, 31.5204, 74.3587, 'Lahore Badami Bagh Mandi', 2700.0, CURRENT_TIMESTAMP FROM users WHERE phone_or_email = '03211110001'
ON CONFLICT (buyer_id) DO UPDATE SET preferred_crops = EXCLUDED.preferred_crops;

INSERT INTO buyer_preferences (buyer_id, preferred_crops, preferred_grade, min_qty, max_qty, latitude, longitude, location, max_budget_price, updated_at)
SELECT id, 'Tomato,Wheat', 'A', 1000.0, 8000.0, 30.1575, 71.5249, 'Multan Ghalla Mandi', 2500.0, CURRENT_TIMESTAMP FROM users WHERE phone_or_email = '03211110002'
ON CONFLICT (buyer_id) DO UPDATE SET preferred_crops = EXCLUDED.preferred_crops;

INSERT INTO buyer_preferences (buyer_id, preferred_crops, preferred_grade, min_qty, max_qty, latitude, longitude, location, max_budget_price, updated_at)
SELECT id, 'Potato,Wheat', 'B', 3000.0, 20000.0, 31.4504, 73.1350, 'Faisalabad Sammundri Rd Mandi', 2600.0, CURRENT_TIMESTAMP FROM users WHERE phone_or_email = '03211110003'
ON CONFLICT (buyer_id) DO UPDATE SET preferred_crops = EXCLUDED.preferred_crops;

INSERT INTO buyer_preferences (buyer_id, preferred_crops, preferred_grade, min_qty, max_qty, latitude, longitude, location, max_budget_price, updated_at)
SELECT id, 'Wheat,Potato', 'A', 1500.0, 12000.0, 30.6682, 73.1114, 'Sahiwal Grain Market', 2800.0, CURRENT_TIMESTAMP FROM users WHERE phone_or_email = '03211110004'
ON CONFLICT (buyer_id) DO UPDATE SET preferred_crops = EXCLUDED.preferred_crops;

INSERT INTO buyer_preferences (buyer_id, preferred_crops, preferred_grade, min_qty, max_qty, latitude, longitude, location, max_budget_price, updated_at)
SELECT id, 'Potato,Tomato,Wheat', 'B', 2000.0, 10000.0, 33.5651, 73.0169, 'Rawalpindi Sabzi Mandi I-11', 2750.0, CURRENT_TIMESTAMP FROM users WHERE phone_or_email = '03211110005'
ON CONFLICT (buyer_id) DO UPDATE SET preferred_crops = EXCLUDED.preferred_crops;

-- 4. 20 Produce Listings
INSERT INTO listings (farmer_id, crop, grade, quantity, asking_price, latitude, longitude, location, status, created_at)
VALUES
    ((SELECT id FROM users WHERE phone_or_email='03001112233'), 'Potato', 'A', 8000.0, 2450.0, 30.8081, 73.4458, 'Okara Bypass Farm', 'active', CURRENT_TIMESTAMP - INTERVAL '1 day'),
    ((SELECT id FROM users WHERE phone_or_email='03001112233'), 'Potato', 'A', 12000.0, 2400.0, 30.8120, 73.4510, 'Okara Depalpur Road', 'active', CURRENT_TIMESTAMP - INTERVAL '2 day'),
    ((SELECT id FROM users WHERE phone_or_email='03002223344'), 'Potato', 'B', 5000.0, 2200.0, 30.6682, 73.1114, 'Sahiwal Chichawatni Farm', 'active', CURRENT_TIMESTAMP - INTERVAL '2 day'),
    ((SELECT id FROM users WHERE phone_or_email='03002223344'), 'Potato', 'A', 15000.0, 2550.0, 30.6750, 73.1200, 'Sahiwal Harappa Bypass', 'active', CURRENT_TIMESTAMP - INTERVAL '3 day'),
    ((SELECT id FROM users WHERE phone_or_email='03004445566'), 'Potato', 'B', 6000.0, 2300.0, 31.4504, 73.1350, 'Faisalabad Jhang Rd Farm', 'active', CURRENT_TIMESTAMP - INTERVAL '4 day'),
    ((SELECT id FROM users WHERE phone_or_email='03001112233'), 'Potato', 'C', 4000.0, 1950.0, 30.7900, 73.4200, 'Okara Renala Khurd', 'active', CURRENT_TIMESTAMP - INTERVAL '5 day'),
    ((SELECT id FROM users WHERE phone_or_email='03002223344'), 'Potato', 'A', 10000.0, 2500.0, 30.6800, 73.1000, 'Sahiwal Noor Shah', 'deal_pending', CURRENT_TIMESTAMP - INTERVAL '6 day'),

    ((SELECT id FROM users WHERE phone_or_email='03003334455'), 'Tomato', 'A', 3500.0, 2600.0, 30.1575, 71.5249, 'Multan Shujabad Farm', 'active', CURRENT_TIMESTAMP - INTERVAL '1 day'),
    ((SELECT id FROM users WHERE phone_or_email='03003334455'), 'Tomato', 'A', 4500.0, 2550.0, 30.1800, 71.5500, 'Multan Bosan Road Farm', 'active', CURRENT_TIMESTAMP - INTERVAL '2 day'),
    ((SELECT id FROM users WHERE phone_or_email='03003334455'), 'Tomato', 'B', 2500.0, 2350.0, 30.1200, 71.4900, 'Multan Makhdoom Rashid', 'active', CURRENT_TIMESTAMP - INTERVAL '3 day'),
    ((SELECT id FROM users WHERE phone_or_email='03001112233'), 'Tomato', 'A', 3000.0, 2700.0, 30.8081, 73.4458, 'Okara Hujra Shah Muqeem', 'active', CURRENT_TIMESTAMP - INTERVAL '3 day'),
    ((SELECT id FROM users WHERE phone_or_email='03004445566'), 'Tomato', 'B', 2000.0, 2400.0, 31.4200, 73.1100, 'Faisalabad Tandlianwala', 'active', CURRENT_TIMESTAMP - INTERVAL '4 day'),
    ((SELECT id FROM users WHERE phone_or_email='03003334455'), 'Tomato', 'C', 1800.0, 2100.0, 30.1400, 71.5100, 'Multan Lar Farm Block', 'sold', CURRENT_TIMESTAMP - INTERVAL '7 day'),

    ((SELECT id FROM users WHERE phone_or_email='03004445566'), 'Wheat', 'A', 18000.0, 2800.0, 31.4504, 73.1350, 'Faisalabad Sammundri Belt', 'active', CURRENT_TIMESTAMP - INTERVAL '1 day'),
    ((SELECT id FROM users WHERE phone_or_email='03004445566'), 'Wheat', 'A', 20000.0, 2850.0, 31.4700, 73.1500, 'Faisalabad Chak Jhumra', 'active', CURRENT_TIMESTAMP - INTERVAL '2 day'),
    ((SELECT id FROM users WHERE phone_or_email='03002223344'), 'Wheat', 'A', 14000.0, 2750.0, 30.6682, 73.1114, 'Sahiwal Kassowal Fields', 'active', CURRENT_TIMESTAMP - INTERVAL '3 day'),
    ((SELECT id FROM users WHERE phone_or_email='03002223344'), 'Wheat', 'B', 9000.0, 2650.0, 30.6900, 73.1300, 'Sahiwal Ghaziabad', 'active', CURRENT_TIMESTAMP - INTERVAL '4 day'),
    ((SELECT id FROM users WHERE phone_or_email='03003334455'), 'Wheat', 'A', 16000.0, 2780.0, 30.1575, 71.5249, 'Multan Jalalpur Pirwala', 'active', CURRENT_TIMESTAMP - INTERVAL '4 day'),
    ((SELECT id FROM users WHERE phone_or_email='03001112233'), 'Wheat', 'B', 11000.0, 2600.0, 30.8081, 73.4458, 'Okara Mandi Ahmadabad', 'active', CURRENT_TIMESTAMP - INTERVAL '5 day'),
    ((SELECT id FROM users WHERE phone_or_email='03004445566'), 'Wheat', 'A', 25000.0, 2820.0, 31.4300, 73.1200, 'Faisalabad Jaranwala Gate', 'active', CURRENT_TIMESTAMP - INTERVAL '6 day');
