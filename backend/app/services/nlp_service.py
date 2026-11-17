"""
AgriMate AI - Multilingual Agricultural NLP & Intent Router
Supports English, Urdu (اردو), and Roman Urdu.
Extracts:
- Intents: disease, pest, fertilizer, price, sell
- Entities: crop, symptom, location
Routes to the appropriate application module and expands queries for precision vector retrieval.
"""

import re
from typing import Dict, List, Any, Optional

# Synonyms dictionary for Urdu, Roman Urdu, and English
CROP_SYNONYMS = {
    "Cotton": ["cotton", "kapas", "phutti", "کپاس", "پھٹی", "ruiee"],
    "Wheat": ["wheat", "gandum", "kanak", "گندم", "کنک"],
    "Rice": ["rice", "chawal", "dhan", "paddy", "basmati", "چاول", "دھان", "باسمتی"],
    "Sugarcane": ["sugarcane", "kamad", "ganna", "کماد", "گنا"],
    "Potato": ["potato", "aaloo", "aloo", "آلو"],
    "Tomato": ["tomato", "tamatar", "ٹماٹر"],
    "Maize": ["maize", "corn", "makai", "makki", "مکئی"],
    "Citrus": ["citrus", "kinnow", "kinnu", "malta", "کینو", "مالٹا"],
    "Mango": ["mango", "aam", "آم"]
}

SYMPTOM_SYNONYMS = {
    "Whitefly": ["whitefly", "safaid makhi", "chitti makhi", "safed makhi", "سفید مکھی"],
    "Leaf Curl": ["leaf curl", "curl", "marora", "maror", "patta maror", "پتہ مروڑ", "مروڑا"],
    "Yellow Rust": ["yellow rust", "stripe rust", "zard kangi", "peeli kangi", "زرد کنگی", "پلی کنگی"],
    "Brown Rust": ["brown rust", "leaf rust", "bhoori kangi", "بھوری کنگی"],
    "Blight": ["blight", "early blight", "late blight", "jhalsao", "jhalas", "جھلساؤ", "اگیتا جھلساؤ", "پچھیتا جھلساؤ"],
    "Pink Bollworm": ["pink bollworm", "gulabi sundi", "sundi", "گلابی سنڈی", "سنڈی"],
    "Jassid": ["jassid", "subz tela", "sabz tela", "churda", "سبز تیلا"],
    "Yellowing": ["yellowing", "peela", "zard", "peelay pattay", "پیلے پتے"],
    "Wilting": ["wilting", "murjhana", "sukha", "مرجھانا", "سوکھا"]
}

INTENT_KEYWORDS = {
    "fertilizer": [
        "fertilizer", "urea", "dap", "potash", "sop", "mop", "khaad", "khad", "zinc", 
        "boron", "nitrogen", "phosphorus", "dose", "bag", "بوری", "کھاد", "یوریا", "ڈی اے پی"
    ],
    "pest": [
        "pest", "insect", "spray", "makhi", "sundi", "tela", "thrips", "dawa", "dawai", 
        "keera", "keere", "insecticide", "کیڑا", "سپرے", "دوائی", "حشرات"
    ],
    "disease": [
        "disease", "fungus", "virus", "infection", "spots", "curl", "rust", "blight", 
        "beemari", "bimari", "maror", "kangi", "jhalsao", "بیماری", "الجھاؤ", "پھپھوندی"
    ],
    "price": [
        "price", "rate", "cost", "mandi rate", "qeemat", "bhao", "today price", 
        "مارکیٹ", "ریٹ", "قیمت", "بھاؤ", "منڈی ریٹ"
    ],
    "sell": [
        "sell", "sold", "buyer", "demand", "maund", "bechna", "farokht", "khareedari", 
        "بیچنا", "فروخت", "خریدار"
    ]
}

PAKISTANI_LOCATIONS = [
    "multan", "faisalabad", "sahiwal", "khanewal", "bahawalpur", "lahore", "sukkur",
    "hyderabad", "larkana", "mirpurkhas", "peshawar", "mardan", "swat", "quetta",
    "naseerabad", "bhakkar", "layyah", "vehari", "lodhran", "pakpattan", "okara",
    "ملتان", "فیصل آباد", "ساہیوال", "خانیوال", "بہاولپور", "سکھر", "حیدرآباد", "لاہور"
]


def normalize_text(text: str) -> str:
    """Normalizes lowercase, punctuation, and whitespace."""
    clean = text.lower().strip()
    clean = re.sub(r"[?!.,;:_\-\(\)\[\]\"']", " ", clean)
    clean = re.sub(r"\s+", " ", clean)
    return clean


def extract_entities_and_intent(query: str) -> Dict[str, Any]:
    """
    Extracts intents, crop entities, symptom entities, location entities,
    and determines the target module for UI/Backend routing.
    """
    norm = normalize_text(query)
    
    # 1. Detect Intent
    intent_scores = {intent: 0 for intent in INTENT_KEYWORDS}
    for intent, words in INTENT_KEYWORDS.items():
        for w in words:
            if re.search(r"\b" + re.escape(w) + r"\b", norm):
                intent_scores[intent] += 1
                
    best_intent = max(intent_scores, key=intent_scores.get)
    if intent_scores[best_intent] == 0:
        best_intent = "general_inquiry"

    # 2. Extract Crops
    detected_crops = []
    for crop_canonical, variants in CROP_SYNONYMS.items():
        for v in variants:
            if re.search(r"\b" + re.escape(v) + r"\b", norm):
                detected_crops.append(crop_canonical)
                break

    # 3. Extract Symptoms
    detected_symptoms = []
    for symptom_canonical, variants in SYMPTOM_SYNONYMS.items():
        for v in variants:
            if re.search(r"\b" + re.escape(v) + r"\b", norm):
                detected_symptoms.append(symptom_canonical)
                break

    # 4. Extract Location
    detected_location = None
    for loc in PAKISTANI_LOCATIONS:
        if re.search(r"\b" + re.escape(loc) + r"\b", norm):
            detected_location = loc.title()
            break

    # 5. Route Module Recommendation
    route_module = "ADVISORY_RAG"
    if best_intent == "sell":
        route_module = "MARKETPLACE_SELL"
    elif best_intent == "price":
        route_module = "MARKETPLACE_PRICES"
    elif best_intent == "disease" and any(s in ["Leaf Curl", "Rust", "Blight", "Yellowing"] for s in detected_symptoms):
        route_module = "DISEASE_CAMERA_SCAN"

    # Formulate expanded vector search query (canonical expansion)
    expansion_terms = []
    if detected_crops:
        expansion_terms.extend(detected_crops)
    if detected_symptoms:
        expansion_terms.extend(detected_symptoms)
    if best_intent in ["fertilizer", "pest", "disease"]:
        expansion_terms.append(best_intent)
        
    expanded_search_query = query + " " + " ".join(expansion_terms)

    return {
        "original_query": query,
        "normalized_query": norm,
        "intent": best_intent,
        "entities": {
            "crops": detected_crops,
            "symptoms": detected_symptoms,
            "location": detected_location,
        },
        "route_module": route_module,
        "expanded_query": expanded_search_query.strip()
    }

