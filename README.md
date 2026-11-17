# AgriMate AI: Precision Farming Ecosystem for Pakistan 🌾🇵🇰

AgriMate AI is a production-grade, AI-powered agricultural decision-support ecosystem designed specifically for Pakistani smallholder farmers, grain/commodity mandi buyers, and agronomic extension experts.

---

## Architecture Overview

```
AgriMateAI/
├── backend/                  # Python FastAPI REST Backend & AI Services
│   ├── app/
│   │   ├── api/              # API v1 routers & role dependency injectors
│   │   ├── core/             # Central design tokens, JWT security, Pakistani hubs
│   │   ├── db/               # SQLAlchemy ORM session & connection pooling
│   │   ├── models/           # User, Crop Diary, Disease Scan, Market, Logistics
│   │   └── schemas/          # Pydantic schemas (minimal 5-field registration)
│   ├── db_postgres.sql       # Production PostgreSQL table DDL & seed queries
│   ├── main.py               # Application entrypoint
│   ├── requirements.txt      # Backend dependencies
│   ├── seed_data.py          # Demo user seeder (Farmer, Buyer, Expert)
│   └── test_phase1.py        # Automated test suite (10/10 tests)
│
└── frontend/                 # Flutter Android Mobile App (Material 3)
    ├── assets/               # Branded assets (logo.png, farmer_3d.png, fields)
    ├── lib/
    │   ├── main.dart         # Flutter app entry & system styling
    │   ├── theme/
    │   │   └── app_theme.dart # Strict central theme (zero hardcoded colors)
    │   ├── models/           # UserModel
    │   ├── services/         # ApiService & AuthProvider (JWT session)
    │   ├── screens/
    │   │   ├── splash_screen.dart       # Front screen with assets/logo.png
    │   │   ├── onboarding_screen.dart   # Screen 1 (Hero & 3D Farmer)
    │   │   ├── auth/                    # Minimal Register & Login
    │   │   └── dashboard/
    │   │       ├── farmer_home_screen.dart # Screen 2 (Weather & My Fields)
    │   │       ├── farm_overview_screen.dart # Screen 3 (Gauge & Aerial view)
    │   │       ├── buyer_home_screen.dart  # Mandi procurement console
    │   │       └── expert_home_screen.dart # Diagnostic verification queue
    │   └── widgets/          # SemicircularGauge, AgriLogo, DecisionDisclaimer
    └── pubspec.yaml          # Flutter dependencies & asset registrations
```

---

## Visual Design System & UI Specifications

The mobile app follows a calm, organic, modern aesthetic:
- **Background**: Solid Olive/Moss Green (`#6B8A47`).
- **Cards**: Translucent white at 8–12% opacity with soft rounded corners (`24–32px`, default `28px`), borderless with zero heavy shadows.
- **Accent Color**: Vivid Lime-Yellow (`#F4F23A`), used exclusively for primary buttons, active chips, stat pills, weather highlights, and gauge arcs.
- **Text**: Pure White (`#FFFFFF`) for bold values/headings; White at ~65% opacity (`#A6FFFFFF`) for secondary text; Dark Green (`#253813`) on yellow buttons.
- **Typography**: Geometric sans-serif (`GoogleFonts.outfit`), large hero headings (`36–44px`), medium-weight card titles, and small labels (`12–13px`).
- **Pill Shapes**: Fully rounded pill shapes for all action buttons and filter chips.

---

## Backend Setup (FastAPI + PostgreSQL / SQLite)

### 1. Requirements
- Python 3.10+ (Tested on Python 3.13)
- PostgreSQL (Optional; defaults to zero-config SQLite `agrimate.db` for instant local testing)

### 2. Install Dependencies
```powershell
cd "c:\Users\SMART TECH\Desktop\AgriMateAI\backend"
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Users Table (Optional Production Path)
To use PostgreSQL instead of SQLite:
1. Create a database:
   ```sql
   CREATE DATABASE agrimate_db;
   ```
2. Run the provided schema script:
   ```powershell
   psql -U postgres -d agrimate_db -f db_postgres.sql
   ```
3. Update `backend/.env`:
   ```ini
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/agrimate_db
   ```

### 4. Seed Pakistani Demo Accounts
Populate demo accounts for all three user roles:
```powershell
python seed_data.py
```
*Seeded accounts:*
- **Farmer**: Phone `03001234567` | Password `Password123!` | Location `Multan, Punjab`
- **Buyer**: Phone `03219876543` | Password `Password123!` | Location `Faisalabad, Punjab`
- **Expert/Admin**: Email `expert.farooq@agrimate.pk` | Password `Password123!` | Location `Lahore, Punjab`

### 5. Run Verification Tests
```powershell
python test_phase1.py
```

### 6. Launch Backend Server
```powershell
python main.py
```
- Interactive API Docs: [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)
- Health Endpoint: [http://127.0.0.1:8000/api/v1/system/health](http://127.0.0.1:8000/api/v1/system/health)

---

## Frontend Setup (Flutter Android App)

### 1. Requirements
- Flutter SDK 3.0+
- Android Studio / VS Code with Flutter extension
- Android Device or Emulator

### 2. Fetch Dependencies
```powershell
cd "c:\Users\SMART TECH\Desktop\AgriMateAI\frontend"
flutter pub get
```

### 3. Generate Assets (Already bundled)
The assets have been generated in `frontend/assets/`:
- `logo.png`: High-resolution circular AgriMate emblem.
- `farmer_3d.png`: 3D-styled farmer character holding wheat.
- `field_aerial.jpg`: Lush aerial crop field photo.
- `field_aerial_header.jpg`: Panoramic aerial field header.

### 4. Run the Mobile App
```powershell
flutter run
```
*Tip:* You can use the **1-Tap Demo Accounts** buttons on the Login screen to instantly sign in as Farmer, Buyer, or Expert.

---

## Mandatory System Compliance Rules

1. **One Central Theme File**: [`frontend/lib/theme/app_theme.dart`](file:///c:/Users/SMART%20TECH/Desktop/AgriMateAI/frontend/lib/theme/app_theme.dart) defines all colors, typography, and card decorations. No hardcoded hex color codes exist elsewhere.
2. **AgriMate Logo on Front Screen**: Displayed on the Splash and Login screens from `assets/logo.png`.
3. **Minimal Registration Schema**: Exactly 5 fields:
   - `name`
   - `phone_or_email`
   - `password`
   - `role` (`Farmer`, `Buyer`, `Expert/Admin`)
   - `location` (Pakistani district & province)
4. **Decision-Support Disclaimer**: Injected into all API responses via `X-AgriMate-Decision-Disclaimer` and displayed prominently on mobile UI advisory cards.
5. **Zero Hallucinated Advice**: Advisory citations linked to verified institutions (PARC, NARC, Punjab Agri Extension).

