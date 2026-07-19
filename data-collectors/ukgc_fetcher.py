import io
import os
import json
import zipfile
import csv
import urllib.request
from datetime import datetime

ZIP_URL = "https://gamblingcommission.gov.uk"
OUTPUT_DIR = "processed-data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "uk-casinos.json")

def fetch_and_process_ukgc():
    print("🤖 SlotMetric: Starting UKGC data collection...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        req = urllib.request.Request(ZIP_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            zip_data = response.read()
    except Exception as e:
        print(f"❌ Error downloading UKGC data: {e}")
        return

    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        csv_filename = [f for f in z.namelist() if 'business' in f.lower() and f.endswith('.csv')]
        if not csv_filename:
            print("❌ Could not find the Business CSV inside the UKGC ZIP file.")
            return
            
        print(f"📦 Extracting and processing: {csv_filename}")
        with z.open(csv_filename) as f:
            csv_text = io.TextIOWrapper(f, encoding='utf-8-sig')
            reader = csv.DictReader(csv_text)
            casinos_list = []
            
            for row in reader:
                status = row.get('AccountStatus', '').strip().lower()
                activities = row.get('LicensedActivities', '').strip().lower()
                
                if status == 'active' and 'casino' in activities and 'remote' in activities:
                    brand_name = row.get('AccountName', '').strip()
                    license_num = row.get('AccountNumber', '').strip()
                    website = row.get('WebsiteAddress', '').strip()
                    
                    if not website or website.lower() == 'null':
                        continue
                    
                    casino_entry = {
                        "id": f"uk-{license_num}",
                        "brand_name": brand_name,
                        "official_url": website if website.startswith('http') else f"https://{website}",
                        "affiliate_url": "",
                        "license_number": license_num,
                        "last_updated": datetime.today().strftime('%Y-%m-%d'),
                        "seo_meta": {
                            "card_title": f"{brand_name} UK License Details & Review",
                            "alt_text": f"{brand_name} official logo verified by UKGC"
                        },
                        "features": {
                            "bonus_text": None,
                            "wagering_requirement": None,
                            "average_rtp": None,
                            "payout_speed": None
                        }
                    }
                    casinos_list.append(casino_entry)

            with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_out:
                json.dump(casinos_list, json_out, indent=2, ensure_ascii=False)
                
            print(f"✅ SlotMetric Success: Saved {len(casinos_list)} licensed UK casinos.")

if __name__ == "__main__":
    fetch_and_process_ukgc()
