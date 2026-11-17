"""
AgriMate AI - Core Constants & Business Rules
Pakistani Agricultural Domain, Roles, and Decision Support Disclaimers.
"""

from enum import Enum
from typing import List, Dict


class UserRole(str, Enum):
    FARMER = "Farmer"
    BUYER = "Buyer"
    EXPERT_ADMIN = "Expert/Admin"


# Mandatory Decision-Support Disclaimer for all advisory and diagnostic features
DECISION_SUPPORT_DISCLAIMER_EN = (
    "AgriMate AI provides AI-assisted agricultural advisory and diagnostic support. "
    "All recommendations, disease detections, and treatments are algorithmic estimates and "
    "must not replace official verification by local certified agronomists or Agriculture "
    "Extension Departments. Always test chemical applications on a small sample patch first."
)

DECISION_SUPPORT_DISCLAIMER_UR = (
    "ایگری میٹ اے آئی مصنوعی ذہانت پر مبنی زرعی مشاورتی اور تشخیصی نظام فراہم کرتا ہے۔ "
    "تمام سفارشات اور بیماریوں کی تشخیص تخمینہ جاتی ہیں اور یہ مستند زرعی ماہرین یا محکمہ زراعت "
    "کی باضابطہ رہنمائی کا متبادل نہیں ہیں۔ کیمیائی ادویات کے استعمال سے پہلے مقامی زرعی توسیع افسر سے تصدیق ضرور کریں۔"
)

DECISION_SUPPORT_DISCLAIMER_ROMAN = (
    "AgriMate AI masnooi zehanat (AI) par mabni zarai mashwaray aur tashkhees faraham karta hai. "
    "Tamam sifarishat aur beemariyon ki nishandahi takhmeena hain aur ye mahir-e-ziraat ya "
    "Mehkma-e-Ziraat ki rehnumai ka mutabadil nahi hain. Dawai istemal karnay se pehlay tasdeeq zaroor karein."
)

# Common Agricultural Districts and Hubs in Pakistan
PAKISTANI_AGRI_HUBS: List[Dict[str, str]] = [
    {"district": "Multan", "province": "Punjab", "major_crops": "Cotton, Mango, Wheat"},
    {"district": "Faisalabad", "province": "Punjab", "major_crops": "Wheat, Sugarcane, Maize"},
    {"district": "Bahawalpur", "province": "Punjab", "major_crops": "Cotton, Wheat, Mustard"},
    {"district": "Sahiwal", "province": "Punjab", "major_crops": "Maize, Potato, Wheat, Cotton"},
    {"district": "Rahim Yar Khan", "province": "Punjab", "major_crops": "Sugarcane, Cotton, Wheat"},
    {"district": "Sargodha", "province": "Punjab", "major_crops": "Citrus (Kinnow), Wheat, Sugarcane"},
    {"district": "Khanewal", "province": "Punjab", "major_crops": "Cotton, Wheat, Maize"},
    {"district": "Hyderabad", "province": "Sindh", "major_crops": "Rice, Wheat, Mango, Sugarcane"},
    {"district": "Sukkur", "province": "Sindh", "major_crops": "Dates, Rice, Wheat"},
    {"district": "Larkana", "province": "Sindh", "major_crops": "Rice, Guava, Wheat"},
    {"district": "Mirpur Khas", "province": "Sindh", "major_crops": "Mango, Sugarcane, Cotton"},
    {"district": "Peshawar", "province": "KPK", "major_crops": "Tobacco, Maize, Wheat"},
    {"district": "Mardan", "province": "KPK", "major_crops": "Sugarcane, Tobacco, Maize"},
    {"district": "Swat", "province": "KPK", "major_crops": "Apple, Peach, Maize, Vegetables"},
    {"district": "Quetta", "province": "Balochistan", "major_crops": "Apples, Grapes, Almonds"},
    {"district": "Naseerabad", "province": "Balochistan", "major_crops": "Rice, Wheat, Oilseeds"},
    {"district": "Lasbela", "province": "Balochistan", "major_crops": "Castor, Cotton, Vegetables"}
]

# Central Theme Design Tokens (Strict Single Source of Truth)
CENTRAL_THEME_TOKENS = {
    "palette": {
        "primary": "#2E7D32",       # Emerald Forest Green (Crop health, vibrancy)
        "primaryLight": "#81C784",  # Soft Green (Accent cards, badges)
        "primaryDark": "#1B5E20",   # Deep Canopy Green (App bars, primary buttons)
        "secondary": "#F9A825",     # Golden Harvest (Wheat, ripening, alerts)
        "secondaryLight": "#FFF59D",# Light Amber
        "secondaryDark": "#C17900", # Deep Amber
        "earthClay": "#795548",     # Silt & Fertile Loam (Soil data, borders)
        "background": "#F4F7F4",    # Clean neutral off-white with hint of organic green
        "surface": "#FFFFFF",       # Card surface
        "textPrimary": "#1C251D",   # High-contrast charcoal text
        "textSecondary": "#536353", # Subdued agricultural gray
        "error": "#D32F2F",         # Disease severity high
        "warning": "#ED6C02",       # Moderate disease / logistics alert
        "info": "#0288D1",          # Weather / irrigation notification
        "success": "#2E7D32",       # Optimal crop health / deal matched
    },
    "typography": {
        "fontFamilyEnglish": "Roboto",
        "fontFamilyUrdu": "NotoNastaliqUrdu"
    }
}

