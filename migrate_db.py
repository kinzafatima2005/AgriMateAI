import sqlite3
import os

required_cols = [
    ("growth_stage", "VARCHAR(50) DEFAULT 'Vegetative'"),
    ("entry_date", "TIMESTAMP"),
    ("photo_url", "TEXT"),
    ("disease_prediction", "VARCHAR(120)"),
    ("confidence", "FLOAT DEFAULT 0.0"),
    ("severity", "VARCHAR(50) DEFAULT 'Optimal'"),
    ("notes", "TEXT"),
    ("treatment_applied", "TEXT"),
]

for path in ["agrimate.db", "backend/agrimate.db"]:
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(crop_diary_entries)")
        existing = [c[1] for c in cur.fetchall()]
        print(f"Checking {path}, found {len(existing)} columns")
        for col, col_type in required_cols:
            if col not in existing:
                print(f"Adding {col} to {path}")
                cur.execute(f"ALTER TABLE crop_diary_entries ADD COLUMN {col} {col_type}")
        conn.commit()
        conn.close()

print("Migration completed successfully!")
