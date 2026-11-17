"""
AgriMate AI - Seed Buyer Data Script (SQLite & PostgreSQL Compatible)
Creates:
- 5 Buyer Users with BuyerPreference records
- 20 Produce Listings across Potato, Tomato, Wheat
- Sample Buyer Interests covering all 5 statuses:
  ['interested', 'accepted', 'in_progress', 'completed', 'rejected']
- DealStatusHistory audit records for each interest
- Sample notifications for matches and deal updates
"""

import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine
import app.db.base as _models_base
from app.db.session import Base
from app.models.user import User
from app.models.buyer import BuyerPreference, Listing, BuyerInterest, DealStatusHistory
from app.models.notification import Notification
from app.core.security import get_password_hash
from app.core.constants import UserRole


def seed_all():
    print("[+] Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Farmers for listings
        farmers_data = [
            {"contact": "03001112233", "name": "Haji Ghulam Rasool", "location": "Okara, Punjab", "lat": 30.8081, "lon": 73.4458},
            {"contact": "03002223344", "name": "Chaudhry Akram", "location": "Sahiwal, Punjab", "lat": 30.6682, "lon": 73.1114},
            {"contact": "03003334455", "name": "Malik Riaz", "location": "Multan, Punjab", "lat": 30.1575, "lon": 71.5249},
            {"contact": "03004445566", "name": "Mian Tariq Farooq", "location": "Faisalabad, Punjab", "lat": 31.4504, "lon": 73.1350},
        ]
        
        farmer_objs = {}
        for fd in farmers_data:
            farmer = db.query(User).filter(User.phone_or_email == fd["contact"]).first()
            if not farmer:
                farmer = User(
                    phone_or_email=fd["contact"],
                    hashed_password=get_password_hash("Password123!"),
                    name=fd["name"],
                    role=UserRole.FARMER.value,
                    location=fd["location"],
                    is_active=True
                )
                db.add(farmer)
                db.flush()
            else:
                farmer.name = fd["name"]
                farmer.location = fd["location"]
                db.flush()
            farmer_objs[fd["contact"]] = farmer

        # 2. 5 Buyers
        buyers_data = [
            {
                "contact": "03211110001",
                "name": "Tariq Traders (Lahore Mandi)",
                "location": "Lahore Badami Bagh Mandi",
                "crops": "Potato,Tomato",
                "grade": "A",
                "min_qty": 2000.0,
                "max_qty": 15000.0,
                "lat": 31.5204,
                "lon": 74.3587,
                "budget": 2700.0
            },
            {
                "contact": "03219998877",
                "name": "Lahore Commission Agent",
                "location": "Badami Bagh Mandi, Lahore",
                "crops": "Potato,Tomato,Wheat",
                "grade": "A",
                "min_qty": 2000.0,
                "max_qty": 15000.0,
                "lat": 31.5204,
                "lon": 74.3587,
                "budget": 2700.0
            },
            {
                "contact": "03211110002",
                "name": "Al-Rehman Foods (Multan)",
                "location": "Multan Ghalla Mandi",
                "crops": "Tomato,Wheat",
                "grade": "A",
                "min_qty": 1000.0,
                "max_qty": 8000.0,
                "lat": 30.1575,
                "lon": 71.5249,
                "budget": 2500.0
            },
            {
                "contact": "03211110003",
                "name": "National Agro Processors",
                "location": "Faisalabad Sammundri Rd Mandi",
                "crops": "Potato,Wheat",
                "grade": "B",
                "min_qty": 3000.0,
                "max_qty": 20000.0,
                "lat": 31.4504,
                "lon": 73.1350,
                "budget": 2600.0
            },
            {
                "contact": "03211110004",
                "name": "Bismillah Grain House",
                "location": "Sahiwal Grain Market",
                "crops": "Wheat,Potato",
                "grade": "A",
                "min_qty": 1500.0,
                "max_qty": 12000.0,
                "lat": 30.6682,
                "lon": 73.1114,
                "budget": 2800.0
            },
            {
                "contact": "03211110005",
                "name": "Khyber Mandi Wholesalers",
                "location": "Rawalpindi Sabzi Mandi I-11",
                "crops": "Potato,Tomato,Wheat",
                "grade": "B",
                "min_qty": 2000.0,
                "max_qty": 10000.0,
                "lat": 33.5651,
                "lon": 73.0169,
                "budget": 2750.0
            },
        ]

        buyer_objs = []
        for bd in buyers_data:
            buyer = db.query(User).filter(User.phone_or_email == bd["contact"]).first()
            if not buyer:
                buyer = User(
                    phone_or_email=bd["contact"],
                    hashed_password=get_password_hash("Password123!"),
                    name=bd["name"],
                    role=UserRole.BUYER.value,
                    location=bd["location"],
                    is_active=True
                )
                db.add(buyer)
                db.flush()
            else:
                buyer.role = UserRole.BUYER.value
                buyer.name = bd["name"]
                buyer.location = bd["location"]
                db.flush()

            # Ensure buyer preference exists
            pref = db.query(BuyerPreference).filter(BuyerPreference.buyer_id == buyer.id).first()
            if not pref:
                pref = BuyerPreference(
                    buyer_id=buyer.id,
                    preferred_crops=bd["crops"],
                    preferred_grade=bd["grade"],
                    min_qty=bd["min_qty"],
                    max_qty=bd["max_qty"],
                    latitude=bd["lat"],
                    longitude=bd["lon"],
                    location=bd["location"],
                    max_budget_price=bd["budget"]
                )
                db.add(pref)
            else:
                pref.preferred_crops = bd["crops"]
                pref.preferred_grade = bd["grade"]
                pref.min_qty = bd["min_qty"]
                pref.max_qty = bd["max_qty"]
                pref.latitude = bd["lat"]
                pref.longitude = bd["lon"]
                pref.location = bd["location"]
                pref.max_budget_price = bd["budget"]
            buyer_objs.append(buyer)

        db.commit()

        # 3. 20 Listings across Potato, Tomato, Wheat
        now = datetime.now(timezone.utc)
        listings_seed = [
            # Potato (Okara & Sahiwal heartland)
            {"f_phone": "03001112233", "crop": "Potato", "grade": "A", "qty": 8000.0, "price": 2450.0, "lat": 30.8081, "lon": 73.4458, "loc": "Okara Bypass Farm", "status": "active", "days_ago": 1},
            {"f_phone": "03001112233", "crop": "Potato", "grade": "A", "qty": 12000.0, "price": 2400.0, "lat": 30.8120, "lon": 73.4510, "loc": "Okara Depalpur Road", "status": "active", "days_ago": 2},
            {"f_phone": "03002223344", "crop": "Potato", "grade": "B", "qty": 5000.0, "price": 2200.0, "lat": 30.6682, "lon": 73.1114, "loc": "Sahiwal Chichawatni Farm", "status": "active", "days_ago": 2},
            {"f_phone": "03002223344", "crop": "Potato", "grade": "A", "qty": 15000.0, "price": 2550.0, "lat": 30.6750, "lon": 73.1200, "loc": "Sahiwal Harappa Bypass", "status": "active", "days_ago": 3},
            {"f_phone": "03004445566", "crop": "Potato", "grade": "B", "qty": 6000.0, "price": 2300.0, "lat": 31.4504, "lon": 73.1350, "loc": "Faisalabad Jhang Rd Farm", "status": "active", "days_ago": 4},
            {"f_phone": "03001112233", "crop": "Potato", "grade": "C", "qty": 4000.0, "price": 1950.0, "lat": 30.7900, "lon": 73.4200, "loc": "Okara Renala Khurd", "status": "active", "days_ago": 5},
            {"f_phone": "03002223344", "crop": "Potato", "grade": "A", "qty": 10000.0, "price": 2500.0, "lat": 30.6800, "lon": 73.1000, "loc": "Sahiwal Noor Shah", "status": "deal_pending", "days_ago": 6},
            
            # Tomato (Multan, Khanewal, Okara)
            {"f_phone": "03003334455", "crop": "Tomato", "grade": "A", "qty": 3500.0, "price": 2600.0, "lat": 30.1575, "lon": 71.5249, "loc": "Multan Shujabad Farm", "status": "active", "days_ago": 1},
            {"f_phone": "03003334455", "crop": "Tomato", "grade": "A", "qty": 4500.0, "price": 2550.0, "lat": 30.1800, "lon": 71.5500, "loc": "Multan Bosan Road Farm", "status": "active", "days_ago": 2},
            {"f_phone": "03003334455", "crop": "Tomato", "grade": "B", "qty": 2500.0, "price": 2350.0, "lat": 30.1200, "lon": 71.4900, "loc": "Multan Makhdoom Rashid", "status": "active", "days_ago": 3},
            {"f_phone": "03001112233", "crop": "Tomato", "grade": "A", "qty": 3000.0, "price": 2700.0, "lat": 30.8081, "lon": 73.4458, "loc": "Okara Hujra Shah Muqeem", "status": "active", "days_ago": 3},
            {"f_phone": "03004445566", "crop": "Tomato", "grade": "B", "qty": 2000.0, "price": 2400.0, "lat": 31.4200, "lon": 73.1100, "loc": "Faisalabad Tandlianwala", "status": "active", "days_ago": 4},
            {"f_phone": "03003334455", "crop": "Tomato", "grade": "C", "qty": 1800.0, "price": 2100.0, "lat": 30.1400, "lon": 71.5100, "loc": "Multan Lar Farm Block", "status": "sold", "days_ago": 7},

            # Wheat (Punjab grain belt)
            {"f_phone": "03004445566", "crop": "Wheat", "grade": "A", "qty": 18000.0, "price": 2800.0, "lat": 31.4504, "lon": 73.1350, "loc": "Faisalabad Sammundri Belt", "status": "active", "days_ago": 1},
            {"f_phone": "03004445566", "crop": "Wheat", "grade": "A", "qty": 20000.0, "price": 2850.0, "lat": 31.4700, "lon": 73.1500, "loc": "Faisalabad Chak Jhumra", "status": "active", "days_ago": 2},
            {"f_phone": "03002223344", "crop": "Wheat", "grade": "A", "qty": 14000.0, "price": 2750.0, "lat": 30.6682, "lon": 73.1114, "loc": "Sahiwal Kassowal Fields", "status": "active", "days_ago": 3},
            {"f_phone": "03002223344", "crop": "Wheat", "grade": "B", "qty": 9000.0, "price": 2650.0, "lat": 30.6900, "lon": 73.1300, "loc": "Sahiwal Ghaziabad", "status": "active", "days_ago": 4},
            {"f_phone": "03003334455", "crop": "Wheat", "grade": "A", "qty": 16000.0, "price": 2780.0, "lat": 30.1575, "lon": 71.5249, "loc": "Multan Jalalpur Pirwala", "status": "active", "days_ago": 4},
            {"f_phone": "03001112233", "crop": "Wheat", "grade": "B", "qty": 11000.0, "price": 2600.0, "lat": 30.8081, "lon": 73.4458, "loc": "Okara Mandi Ahmadabad", "status": "active", "days_ago": 5},
            {"f_phone": "03004445566", "crop": "Wheat", "grade": "A", "qty": 25000.0, "price": 2820.0, "lat": 31.4300, "lon": 73.1200, "loc": "Faisalabad Jaranwala Gate", "status": "active", "days_ago": 6},
        ]

        # Clear existing listings to avoid duplications during seed reruns
        db.query(DealStatusHistory).delete()
        db.query(BuyerInterest).delete()
        db.query(Listing).delete()
        db.commit()

        listing_objs = []
        for item in listings_seed:
            f = farmer_objs[item["f_phone"]]
            l = Listing(
                farmer_id=f.id,
                crop=item["crop"],
                grade=item["grade"],
                quantity=item["qty"],
                asking_price=item["price"],
                latitude=item["lat"],
                longitude=item["lon"],
                location=item["loc"],
                status=item["status"],
                created_at=now - timedelta(days=item["days_ago"])
            )
            db.add(l)
            listing_objs.append(l)

        db.flush()

        # 4. Sample Interests covering all 5 statuses:
        # ['interested', 'accepted', 'in_progress', 'completed', 'rejected']
        # Let buyer 0 (Tariq Traders Lahore) have 5 distinct deals across statuses
        tariq_buyer = buyer_objs[0]
        
        sample_interests = [
            {
                "buyer": tariq_buyer,
                "listing": listing_objs[0], # Okara Potato 8000kg
                "status": "interested",
                "offered_price": 2400.0,
                "qty": 5000.0,
                "message": "Interested in 5000kg Grade A Potato. Can pick up within 48 hours.",
                "history": [
                    ("interested", "Initial purchase interest submitted by buyer.", 0)
                ]
            },
            {
                "buyer": tariq_buyer,
                "listing": listing_objs[1], # Okara Potato 12000kg
                "status": "accepted",
                "offered_price": 2380.0,
                "qty": 6000.0,
                "message": "Bulk purchase for Lahore Badami Bagh market supply.",
                "history": [
                    ("interested", "Interest expressed by buyer.", 2),
                    ("accepted", "Farmer Haji Ghulam Rasool accepted offer of PKR 2,380/maund.", 1)
                ]
            },
            {
                "buyer": tariq_buyer,
                "listing": listing_objs[7], # Multan Tomato 3500kg
                "status": "in_progress",
                "offered_price": 2550.0,
                "qty": 2000.0,
                "message": "Require 2000kg fresh Grade A tomatoes dispatched in crates.",
                "history": [
                    ("interested", "Buyer initiated interest for 2000kg Tomato.", 3),
                    ("accepted", "Offer accepted by farmer Malik Riaz.", 2),
                    ("in_progress", "Vehicle dispatched. Quality inspection scheduled at mandi checkpoint.", 1)
                ]
            },
            {
                "buyer": tariq_buyer,
                "listing": listing_objs[12], # Multan Tomato sold
                "status": "completed",
                "offered_price": 2100.0,
                "qty": 1800.0,
                "message": "Delivered to cold chain terminal. Deal successfully settled.",
                "history": [
                    ("interested", "Buyer expressed interest for full lot.", 7),
                    ("accepted", "Farmer accepted PKR 2,100/maund.", 6),
                    ("in_progress", "Logistics transit completed.", 5),
                    ("completed", "Delivery verified, weighbridge slip confirmed. Deal closed.", 4)
                ]
            },
            {
                "buyer": tariq_buyer,
                "listing": listing_objs[3], # Sahiwal Potato 15000kg
                "status": "rejected",
                "offered_price": 2150.0,
                "qty": 10000.0,
                "message": "Offered PKR 2150.",
                "history": [
                    ("interested", "Offer of PKR 2,150 submitted.", 4),
                    ("rejected", "Farmer declined offer: minimum acceptable price was PKR 2,450/maund.", 3)
                ]
            },
            # Also add an interest for buyer 1 (Multan) and buyer 2 (Faisalabad)
            {
                "buyer": buyer_objs[1],
                "listing": listing_objs[8], # Multan Tomato
                "status": "accepted",
                "offered_price": 2500.0,
                "qty": 2500.0,
                "message": "Al-Rehman Foods processing batch #40.",
                "history": [
                    ("interested", "Buyer initiated interest.", 2),
                    ("accepted", "Accepted by farmer.", 1)
                ]
            },
            {
                "buyer": buyer_objs[2],
                "listing": listing_objs[13], # Wheat Faisalabad
                "status": "in_progress",
                "offered_price": 2750.0,
                "qty": 10000.0,
                "message": "National Agro mill purchase order #992.",
                "history": [
                    ("interested", "Offer placed.", 3),
                    ("accepted", "Farmer accepted terms.", 2),
                    ("in_progress", "Weighbridge scheduled at Faisalabad Sammundri.", 1)
                ]
            }
        ]

        for s_int in sample_interests:
            interest = BuyerInterest(
                listing_id=s_int["listing"].id,
                buyer_id=s_int["buyer"].id,
                message=s_int["message"],
                offered_price=s_int["offered_price"],
                quantity_wanted=s_int["qty"],
                status=s_int["status"],
                created_at=now - timedelta(days=s_int["history"][0][2])
            )
            db.add(interest)
            db.flush()

            for hist_status, notes, days_ago in s_int["history"]:
                hist_entry = DealStatusHistory(
                    interest_id=interest.id,
                    status=hist_status,
                    notes=notes,
                    changed_at=now - timedelta(days=days_ago)
                )
                db.add(hist_entry)

        # 5. Seed sample notifications for buyers
        notifications_data = [
            {
                "user_id": tariq_buyer.id,
                "type": "BUYER_MATCH",
                "title": "New High-Match Listing: Potato Grade A",
                "message": "Farmer Haji Ghulam Rasool posted 8,000 kg Potato in Okara (94% Match Score).",
                "is_read": False,
                "days_ago": 0
            },
            {
                "user_id": tariq_buyer.id,
                "type": "DEAL_STATUS",
                "title": "Deal Accepted: 6,000 kg Potato",
                "message": "Farmer accepted your offer of PKR 2,380/maund for Listing #2.",
                "is_read": False,
                "days_ago": 1
            },
            {
                "user_id": tariq_buyer.id,
                "type": "DEAL_STATUS",
                "title": "Deal In-Progress: 2,000 kg Tomato",
                "message": "Farmer Malik Riaz updated deal status to In-Progress. Transport in transit.",
                "is_read": True,
                "days_ago": 2
            },
            {
                "user_id": tariq_buyer.id,
                "type": "BUYER_MATCH",
                "title": "Mandi Rate Alert: Potato Prices Rising",
                "message": "Lahore Badami Bagh mandi rate reached PKR 2,650/40kg today (+4.2%).",
                "is_read": True,
                "days_ago": 3
            }
        ]

        for nd in notifications_data:
            notif = Notification(
                user_id=nd["user_id"],
                notification_type=nd["type"],
                title=nd["title"],
                message=nd["message"],
                is_read=nd["is_read"],
                created_at=now - timedelta(days=nd["days_ago"])
            )
            db.add(notif)

        db.commit()
        print(f"[+] Successfully seeded: 4 Farmers, 5 Buyers with Preferences, 20 Listings, {len(sample_interests)} Deals across all statuses, and {len(notifications_data)} Notifications.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
