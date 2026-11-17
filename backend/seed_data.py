"""
AgriMate AI - Demo Database Seeder
Seeds default users for the 3 target Pakistani roles: Farmer, Buyer, Expert/Admin.
"""

import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash
from app.core.constants import UserRole


def seed_demo_users():
    """Create initial demo users with minimal registration fields."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    demo_accounts = [
        {
            "name": "Muhammad Tariq (Cotton & Wheat Farmer)",
            "phone_or_email": "03001234567",
            "password": "Password123!",
            "role": UserRole.FARMER.value,
            "location": "Multan, Punjab"
        },
        {
            "name": "Haji Abdul Rehman (Grain Mandi Buyer)",
            "phone_or_email": "03219876543",
            "password": "Password123!",
            "role": UserRole.BUYER.value,
            "location": "Faisalabad, Punjab"
        },
        {
            "name": "Dr. Farooq Shah (Agronomy Expert)",
            "phone_or_email": "expert.farooq@agrimate.pk",
            "password": "Password123!",
            "role": UserRole.EXPERT_ADMIN.value,
            "location": "Lahore, Punjab"
        }
    ]
    
    print("\n[AgriMate AI] Seeding initial Pakistani demo accounts...")
    
    for account in demo_accounts:
        existing = db.query(User).filter(User.phone_or_email == account["phone_or_email"]).first()
        if not existing:
            hashed_pwd = get_password_hash(account["password"])
            new_user = User(
                name=account["name"],
                phone_or_email=account["phone_or_email"],
                hashed_password=hashed_pwd,
                role=account["role"],
                location=account["location"],
                is_active=True
            )
            db.add(new_user)
            print(f"  [OK] Created [{account['role']}]: {account['name']} ({account['phone_or_email']}) | {account['location']}")
        else:
            print(f"  [INFO] [{account['role']}] already exists: {account['phone_or_email']}")
            
    db.commit()
    db.close()
    print("[SUCCESS] Seeding completed successfully.\n")


if __name__ == "__main__":
    seed_demo_users()
