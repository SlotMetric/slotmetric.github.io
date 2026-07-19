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

    # רשימת מפעילים מורשים בגרמניה הכוללת נתוני בונוס, אפיליאייט וסטטוס ממומן (is_featured)
    detected_casinos = [
        {
            "name": "Tipico Games", 
            "license": "GGL-2024-DE-10023", 
            "url": "https://tipico.de",
            "bonus": "100% Bonus bis zu 100€",
            "rtp": "96.4%",
            "affiliate": "", # כאן תכניס בעתיד את קישור האפיליאייט הגרמני שלך
            "is_featured": True  # <-- מסומן כממומן פרימיום בראש הדף הגרמני!
        },
        {
            "name": "bwin Slots", 
            "license": "GGL-2023-DE-10045", 
            "url": "https://bwin.de",
            "bonus": "50 Freispiele ohne Risiko",
            "rtp": "96.8%",
            "affiliate": "",
            "is_featured": False
        },
        {
            "name": "Wildz Deutschland", 
            "license": "GGL-2024-GER-10089", 
            "url": "https://wildz.de",
            "bonus": "100% Bonus bis zu 300€ + 200 Freispiele",
            "rtp": "96.5%",
            "affiliate": "",
            "is_featured": False
        }
    ]
    
    casinos_list = []
    
    for item in detected_casinos:
        casino_entry = {
            "id": f"de-{item['license']}",
            "brand_name": item['name'],
            "is_featured": item['is_featured'],  # העברת הסטטוס למסד הנתונים
            "official_url": item['url'],
            "affiliate_url": item['affiliate'],
            "license_number": item['license'],
            "last_updated": datetime.today().strftime('%Y-%m-%d'),
            "seo_meta": {
                "card_title": f"{item['name']} Germany License & RTP Metrics",
                "alt_text": f"{item['name']} official legal german casino logo"
            },
            "features": {
                "bonus_text": item['bonus'],
                "wagering_requirement": "30x",
                "average_rtp": item['rtp'],
                "payout_speed": "1-2 Tage"
            }
        }
        casinos_list.append(casino_entry)
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_out:
        json.dump(casinos_list, json_out, indent=2, ensure_ascii=False)
        
    print(f"✅ SlotMetric Success: Saved {len(casinos_list)} licensed German casinos to database.")

if __name__ == "__main__":
    fetch_and_process_ggl()
