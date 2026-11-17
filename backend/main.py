"""
AgriMate AI - Root Entry Point
Allows running directly with `uvicorn main:app --reload` or `python main.py`
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

