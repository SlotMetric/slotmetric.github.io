import os
import json

TEMPLATE_PATH = "templates/index.html"
OUTPUT_DIR = "public"

# הגדרות מנוע ה-SEO והלוגיקה המודולרית של SlotMetric לכל מדינה
COUNTRIES_CONFIG = {
    "uk": {
        "country_name": "United Kingdom",
        "lang_code": "en",
        "data_file": "processed-data/uk-casinos.json",
        "page_title": "Verified Licensed Casinos in the UK | SlotMetric",
        "meta_description": "Check the official list of UKGC licensed online casinos. Real-time data verification, licensing numbers, and features on SlotMetric."
    },
    "de": {
        "country_name": "Germany (Deutschland)",
        "lang_code": "de",
        "data_file": "processed-data/germany-casinos.json",
        "page_title": "Erlaubte Online Casinos in Deutschland | SlotMetric",
        "meta_description": "Offizielle Whitelist der GGL für Online Casinos in Deutschland. Überprüfte Lizenzen, RTP-Werte und Bonus-Metriken auf SlotMetric."
    },
    "nl": {
        "country_name": "Netherlands (Nederland)",
        "lang_code": "nl",
        "data_file": "processed-data/netherlands-casinos.json",
        "page_title": "Legale Online Casino's in Nederland | SlotMetric",
        "meta_description": "Bekijk de officiële Ksa kansspelvergunninghouders. Betrouwbare online casino's, live RTP-data en bonussen op SlotMetric."
    }
}

def load_template():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"❌ Template file missing at: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def build_casino_cards(json_path):
    # הגנה: אם קובץ הנתונים עדיין לא נוצר על ידי ה-Collector, נציג הודעה זמנית ולא נשבור את האתר
    if not os.path.exists(json_path):
        print(f"⚠️ Data file not found for: {json_path}. Creating placeholder card.")
        return """
        <div class="casino-card" style="border-top-color: #666;">
            <div class="card-header">
                <h2>Database Syncing...</h2>
                <span class="license-badge">Updating Live Data</span>
            </div>
            <div class="features-box">
                <p>We are currently fetching and verifying the regulatory database for this country. Please refresh in a few moments.</p>
            </div>
        </div>
        """
        
    with open(json_path, "r", encoding="utf-8") as f:
        casinos = json.load(f)
        
    cards_html = []
    
    # מגבילים ל-100 המפעילים הראשונים לטובת מהירות טעינה וביצועי Core Web Vitals של גוגל
    for casino in casinos[:100]: 
        # שלב ב': הכנה לבונוסים ו-RTP. אם הם ריקים כרגע, המערכת תציג טקסט אלטרנטיבי חכם
        bonus = casino.get("features", {}).get("bonus_text") or "Reviewing Bonus Terms"
        rtp = casino.get("features", {}).get("average_rtp") or "Calculating Metrics"
        
        # בחירת הקישור: אם הזנו אפיליאייט נשתמש בו, אחרת נפנה זמנית לאתר הרשמי
        target_url = casino.get("affiliate_url") or casino.get("official_url") or "#"
        
        card = f"""
        <div class="casino-card">
            <div class="card-header">
                <h2>{casino['brand_name']}</h2>
                <span class="license-badge">Verified License: #{casino['license_number']}</span>
            </div>
            <div class="features-box">
                <div class="feature-item"><span>Welcome Bonus:</span> <strong>{bonus}</strong></div>
                <div class="feature-item"><span>Average RTP:</span> <strong>{rtp}</strong></div>
            </div>
            <a href="{target_url}" class="btn-play" rel="nofollow noreferrer" target="_blank">Verify & Play</a>
        </div>
        """
        cards_html.append(card)
        
    return "\n".join(cards_html)

def main():
    print("Code Execution: Starting static website build for SlotMetric...")
    template = load_template()
    
    # יצירת תיקיית public הראשית אם אינה קיימת
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # רצה בלולאה ומחוללת עמוד SEO עצמאי לכל מדינה
    for code, config in COUNTRIES_CONFIG.items():
        print(f"📦 Processing country layout for: {config['country_name']} ({code})")
        
        # 1. יצירת קוד ה-HTML של הכרטיסיות
        cards_html = build_casino_cards(config["data_file"])
        
        # 2. הזרקת הנתונים וה-Meta Tags לתוך ה-Template
        page_content = template
        page_content = page_content.replace("{{PAGE_TITLE}}", config["page_title"])
        page_content = page_content.replace("{{META_DESCRIPTION}}", config["meta_description"])
        page_content = page_content.replace("{{LANG_CODE}}", config["lang_code"])
        page_content = page_content.replace("{{COUNTRY_CODE}}", code)
        page_content = page_content.replace("{{COUNTRY_NAME}}", config["country_name"])
        page_content = page_content.replace("{{CASINO_CARDS}}", cards_html)
        
        # 3. יצירת תיקיית המדינה (למשל public/uk/ או public/de/) ושמירת הקובץ
        country_dir = os.path.join(OUTPUT_DIR, code)
        if not os.path.exists(country_dir):
            os.makedirs(country_dir)
            
        output_file_path = os.path.join(country_dir, "index.html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(page_content)
            
    # SEO Redirect: יצירת דף אינדקס ראשי בכתובת המקורית שמפנה אוטומטית לעמוד של בריטניה
    # בצורה זו הגולש שמגיע ל-slotmetric.github.io יועבר מיד לעמוד הפעיל
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write('<html><head><meta http-equiv="refresh" content="0; url=/uk/"></head><body>Redirecting to SlotMetric...</body></html>')

    print("✅ Success: All static pages have been successfully generated in the /public folder.")

if __name__ == "__main__":
    main()
