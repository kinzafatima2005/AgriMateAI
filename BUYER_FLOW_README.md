# AgriMate AI - Buyer Dashboard & Procurement Hub

The Buyer Dashboard provides a tailored procurement and trade-matching workflow for commercial agricultural buyers, commission agents (Arhtis), and food processors across Pakistan.

---

## 🎨 New Official App Logo
- **Concept**: A young, vibrant green plant sprout emerging elegantly from a warm terracotta-brown / warm orange harvest crate/basket.
- **Symbolism**:
  - **Sprout with two leaves**: Represents AI crop advisory, agronomic health, diagnostic recovery, and plant growth.
  - **Basket / Crate**: Represents the agricultural marketplace, commodity procurement, and cold storage / logistics.
- **File Asset**: Located at [`frontend/assets/logo.png`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/assets/logo.png) and embedded across the Flutter app (`AgriLogo`) and mobile web views.

---

## 🛡️ Role-Based Scope & Security Enforcements
- **RBAC Enforcement**: All backend endpoints under `/api/v1/buyer/*` are guarded by `require_role([UserRole.BUYER])`.
- **403 Forbidden**: If a Farmer or Expert user calls any Buyer endpoint, the backend returns `403 Forbidden` (`Access denied. Requires one of roles: Buyer`).
- **Disclaimers**: A mandatory **Decision-support prototype: no payments or legal contracts** notice banner is displayed on the Deals and Overview screens.
- **Strict Theme**: Built exclusively using `AgriColors`, `AgriDimensions`, and `AppTheme` with zero hardcoded colors.

---

## 🗄️ Database Architecture (PostgreSQL & SQLite)
1. **`buyer_preferences`**: `buyer_id`, `preferred_crops`, `preferred_grade`, `min_qty`, `max_qty`, `latitude`, `longitude`, `location`, `max_budget_price`, `updated_at`.
2. **`listings`**: `id`, `farmer_id`, `crop`, `grade`, `quantity`, `asking_price`, `location`, `latitude`, `longitude`, `status`, `created_at`.
3. **`interests`**: `id`, `listing_id`, `buyer_id`, `message`, `offered_price`, `quantity_wanted`, `status` (`interested`, `accepted`, `in_progress`, `completed`, `rejected`), `created_at`, `updated_at`.
4. **`deal_status_history`**: `id`, `interest_id`, `status`, `notes`, `changed_at`.
5. **`notifications`**: `id`, `user_id`, `notification_type` (`BUYER_MATCH`, `DEAL_STATUS`), `title`, `message`, `is_read`, `created_at`.

---

## ⚡ 100-Point Deterministic Matching Engine
Located at [`backend/app/services/matching_service.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/app/services/matching_service.py):
1. **Crop Match (Mandatory Gate)**: If the listing crop does not match the buyer's preferred commodity list, the score is **0%** and the listing is excluded.
2. **Quantity Fit (25%)**: Evaluated against the buyer's min/max demand volume range.
3. **Distance Fit (25%)**: Computed via the Great-Circle Haversine formula over road distance matrices.
4. **Grade Fit (25%)**: Quality hierarchy scoring (A: 3, B: 2, C: 1).
5. **Price Fit (25%)**: Economic feasibility comparing farmer asking price against buyer target budget.

---

## 📱 Deliverables & File Structure

### 1. Flutter Mobile App (`frontend/lib`)
- **Theme**: [`frontend/lib/theme/app_theme.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/theme/app_theme.dart)
- **Models**: [`frontend/lib/models/buyer_models.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/models/buyer_models.dart)
- **API Client**: [`frontend/lib/services/buyer_api_service.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/services/buyer_api_service.dart)
- **State Management**: [`frontend/lib/services/buyer_provider.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/services/buyer_provider.dart)
- **Widgets**:
  - [`frontend/lib/widgets/buyer/buyer_match_radar_card.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/buyer_match_radar_card.dart) (5-factor explainable match breakdown)
  - [`frontend/lib/widgets/buyer/listing_card.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/listing_card.dart)
  - [`frontend/lib/widgets/buyer/deal_card.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/deal_card.dart)
  - [`frontend/lib/widgets/buyer/deal_timeline_widget.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/deal_timeline_widget.dart)
  - [`frontend/lib/widgets/buyer/filter_bottom_sheet.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/filter_bottom_sheet.dart)
  - [`frontend/lib/widgets/buyer/express_interest_dialog.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/express_interest_dialog.dart)
  - [`frontend/lib/widgets/buyer/state_views.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/widgets/buyer/state_views.dart)
- **Screens**:
  - [`frontend/lib/screens/dashboard/buyer/buyer_main_screen.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/buyer_main_screen.dart)
  - [`frontend/lib/screens/dashboard/buyer/tabs/buyer_home_tab.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/tabs/buyer_home_tab.dart)
  - [`frontend/lib/screens/dashboard/buyer/tabs/buyer_listings_tab.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/tabs/buyer_listings_tab.dart)
  - [`frontend/lib/screens/dashboard/buyer/listing_detail_screen.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/listing_detail_screen.dart)
  - [`frontend/lib/screens/dashboard/buyer/tabs/buyer_deals_tab.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/tabs/buyer_deals_tab.dart)
  - [`frontend/lib/screens/dashboard/buyer/deal_detail_screen.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/deal_detail_screen.dart)
  - [`frontend/lib/screens/dashboard/buyer/tabs/buyer_notifications_tab.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/tabs/buyer_notifications_tab.dart)
  - [`frontend/lib/screens/dashboard/buyer/tabs/buyer_profile_tab.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/screens/dashboard/buyer/tabs/buyer_profile_tab.dart)

### 2. FastAPI Backend
- **Buyer Endpoints**: [`backend/app/api/v1/endpoints/buyer.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/app/api/v1/endpoints/buyer.py)
- **Schemas**: [`backend/app/schemas/buyer.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/app/schemas/buyer.py)
- **Database Models**: [`backend/app/models/buyer.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/app/models/buyer.py)
- **SQL Migrations**:
  - DDL Schema: [`backend/migrations/buyer_schema.sql`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/migrations/buyer_schema.sql)
  - Seed Data: [`backend/migrations/seed_buyer_data.sql`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/migrations/seed_buyer_data.sql)
  - Python Seeder: [`backend/seed_buyer_data.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/seed_buyer_data.py)

### 3. Automated Tests
- **Matching Engine Unit Tests (8/8 Passed)**: [`backend/tests/test_matching_engine.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/tests/test_matching_engine.py)
- **Buyer Flow Integration Tests (8/8 Passed)**: [`backend/tests/test_buyer_flow.py`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/backend/tests/test_buyer_flow.py)
- **Flutter Widget Tests**: [`frontend/test/buyer_widgets_test.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/test/buyer_widgets_test.dart)

---

## 🚀 How to Test the Buyer Flow

### Step 1: Ensure Backend & Seed Data Are Active
```bash
python backend/seed_buyer_data.py
python -m uvicorn backend.app.main:app --port 8000 --reload
```

### Step 2: Log in as a Buyer
- **Phone**: `03211110001` or `03219998877`
- **Password**: `Password123!`
- **Name**: Tariq Traders (Lahore Mandi) / Lahore Commission Agent
- The app automatically routes directly to the **Buyer Hub** and restricts access to buyer-only navigation.

### Step 3: Browse and Filter Produce Listings
1. Navigate to the **Listings** tab.
2. Tap the filter button (slider icon) to open the **Filter Bottom Sheet**.
3. Select crop: **Potato**, grade: **Grade A**, minimum quantity slider, or maximum distance radius.
4. Tap **Apply Filters & Sort** to view listings dynamically scored by the deterministic matching engine.

### Step 4: Inspect Listing Detail & 5-Factor Match Radar
1. Tap any produce listing card (e.g. *Okara Potato Lot #1*).
2. Review the **Match Affinity Score**:
   - ✅ **Crop Match Gate**: Passed (Potato matches preferred crops).
   - 📊 **Quantity Fit**: Score out of 25.
   - 📍 **Distance Fit**: Score out of 25 with road distance.
   - 🌟 **Grade Fit**: Score out of 25.
   - 💰 **Price Fit**: Score out of 25 against your budget.

### Step 5: Express Purchase Interest
1. Tap **Express Purchase Interest** at the bottom of the listing detail screen.
2. Adjust your **Offered Price (PKR/40kg)** and **Quantity Wanted (kg)**.
3. Tap **Submit Interest**.
4. The button transitions to disabled with **Interest Already Sent**, preventing duplicate bids.
5. An in-app notification is automatically dispatched to the farmer.

### Step 6: Track Deal Lifecycle in "My Deals"
1. Switch to the **My Deals** tab.
2. Filter through the status tabs: **Interested**, **Accepted**, **In Progress**, **Completed**, **Rejected**.
3. Tap the newly created deal to view the **Deal Lifecycle Audit Timeline** (`deal_status_history`).

### Step 7: Check Notifications
1. Switch to the **Alerts** tab (bell icon).
2. View match alerts and deal status updates.
3. Tap any unread notification to mark it as read.
