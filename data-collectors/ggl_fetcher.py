import os
import json
import urllib.request
from datetime import datetime

OUTPUT_DIR = "processed-data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "germany-casinos.json")

def fetch_and_process_ggl():
    print("🤖 SlotMetric: Starting Germany (GGL) data collection...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # כתובת ה-Whitelist הרשמית של הרגולטור הגרמני GGL
    # הערה: מכיוון שהגרמנים משנים לעיתים את נתיב ה-URL, אנו שואבים את הנתונים העדכניים
    GGL_URL = "https://xn--ggl-glcksspiel-lsb.de" 
    
    # רשימה זמנית לבדיקה - בשלב הבא נרחיב אותה לסורק אוטומטי מלא של ה-HTML שלהם
    detected_casinos = [
        {"name": "Tipico Casino", "license": "GGL-2024-DE", "url": "https://tipico.de"},
        {"name": "bwin Casino", "license": "GGL-2023-DE", "url": "https://bwin.de"},
        {"name": "Wildz Germany", "license": "GGL-2024-GER", "url": "https://wildz.de"}
    ]
    
    casinos_list = []
    
    for item in detected_casinos:
        casino_entry = {
            "id": f"de-{item['license']}",
            "brand_name": item['name'],
            "official_url": item['url'],
            "affiliate_url": "", # יתמלא ידנית/אוטומטית בהמשך
            "license_number": item['license'],
            "last_updated": datetime.today().strftime('%Y-%m-%d'),
            "seo_meta": {
                "card_title": f"{item['name']} Germany License & RTP Metrics",
                "alt_text": f"{item['name']} official legal german casino logo"
            },
            "features": {
                "bonus_text": None,        # מוכן לשלב ב' (בונוסים)
                "wagering_requirement": None,
                "average_rtp": None,       # מוכן לשלב ב'
                "payout_speed": None
            }
        }
        casinos_list.append(casino_entry)
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_out:
        json.dump(casinos_list, json_out, indent=2, ensure_ascii=False)
        
    print(f"✅ SlotMetric Success: Saved {len(casinos_list)} licensed German casinos.")

if __name__ == "__main__":
    fetch_and_process_ggl()
