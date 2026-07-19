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
        "meta_description": "Bekijk de officiële Ksa kansspelvergunninghouders. Betrouwbare online casino's, live RTP-data und bonussen op SlotMetric."
    }
}

def load_template():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"❌ Template file missing at: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def build_casino_cards(json_path):
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
        
    # =========================================================================
    # 🧠 אלגוריתם הדירוג והסינון של SLOTMETRIC (TOP 10 ENGINE)
    # =========================================================================
    # בעתיד, כאשר ה-Scraper יאסוף את הנתונים, הנוסחה תתבסס על 4 הפרמטרים הבאים:
    # 1. אחוז ה-RTP (משקל: 30%) - החזר גבוה לשחקן מעלה את הציון.
    # 2. גובה הבונוס ותנאי הגלגול / Wagering (משקל: 30%) - תנאים קלים מעניקים בונוס לציון.
    # 3. מהירות המשיכה / Payout Speed (משקל: 20%) - תשלום מהיר (Instant/1 Day) מקפיץ קדימה.
    # 4. המרה מסחרית (משקל: 20%) - עמלות שותפים אופטימליות לאתר.
    # =========================================================================
    
    for casino in casinos:
        try:
            # לוגיקת המרה בסיסית לשלב א' (RTP בלבד כבסיס זמני למיונים): לקוח "96.5%" והופך למספר 96.5
            rtp_val = float(casino.get("features", {}).get("average_rtp", "96").replace("%", ""))
            casino["calculated_score"] = round((rtp_val - 90) * 10, 1) # מייצר ציון בטווח של 6.0 עד 10.0
            if casino["calculated_score"] > 10.0: casino["calculated_score"] = 10.0
            if casino["calculated_score"] < 1.0: casino["calculated_score"] = 5.0
        except:
            casino["calculated_score"] = 8.5 # ציון ברירת מחדל אובייקטיבי אם חסר נתון
            
    # הפרדה אסטרטגית בין בתי קזינו ממומנים/שותפי פרימיום לבין שאר הרשימה האובייקטיבית
    featured_casinos = [c for c in casinos if c.get("is_featured") == True]
    regular_casinos = [c for c in casinos if not c.get("is_featured") == True]
    
    # הפעלת המיון של האלגוריתם על הרשימה הרגילה (מהציון הגבוה ביותר לנמוך ביותר)
    regular_casinos.sort(key=lambda x: x["calculated_score"], reverse=True)
    
    # בניית העשירייה הפותחת (TOP 10): 
    # לוקח מקסימום 2 ממומנים לראש הדף, ומשלים בדיוק את החסר מתוך הרגילים הכי טובים בעלי הציון הגבוה ביותר.
    final_list = featured_casinos[:2] + regular_casinos[:(10 - len(featured_casinos[:2]))]
    
    cards_html = []
    
    for casino in final_list:
        is_featured = casino.get("is_featured") == True
        bonus = casino.get("features", {}).get("bonus_text") or "Reviewing Bonus Terms"
        rtp = casino.get("features", {}).get("average_rtp") or "Calculating Metrics"
        target_url = casino.get("affiliate_url") or casino.get("official_url") or "#"
        
        # התאמת מחלקות עיצוב ותגיות SEO בהתאם לסטטוס הכרטיסייה (ממומן או אובייקטיבי)
        card_class = "casino-card featured" if is_featured else "casino-card"
        badge_html = '<span class="sponsored-tag">★ Sponsored TOP</span>' if is_featured else f'<span class="score-tag">Rating: {casino["calculated_score"]}/10</span>'
        rel_tag = 'rel="sponsored nofollow"' if is_featured else 'rel="nofollow noreferrer"'
        
        card = f"""
        <div class="{card_class}">
            <div class="card-header">
                <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 5px;">
                    <h2>{casino['brand_name']}</h2>
                    {badge_html}
                </div>
                <span class="license-badge">Verified License: #{casino['license_number']}</span>
            </div>
            <div class="features-box">
                <div class="feature-item"><span>Welcome Bonus:</span> <strong>{bonus}</strong></div>
                <div class="feature-item"><span>Average RTP:</span> <strong>{rtp}</strong></div>
            </div>
            <a href="{target_url}" class="btn-play" {rel_tag} target="_blank">Verify & Play</a>
        </div>
        """
        cards_html.append(card)
        
    return "\n".join(cards_html)

def main():
    print("Starting static website build for SlotMetric...")
    template = load_template()
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    for code, config in COUNTRIES_CONFIG.items():
        print(f"📦 Processing country layout for: {config['country_name']} ({code})")
        cards_html = build_casino_cards(config["data_file"])
        
        page_content = template
        page_content = page_content.replace("{{PAGE_TITLE}}", config["page_title"])
        page_content = page_content.replace("{{META_DESCRIPTION}}", config["meta_description"])
        page_content = page_content.replace("{{LANG_CODE}}", config["lang_code"])
        page_content = page_content.replace("{{COUNTRY_CODE}}", code)
        page_content = page_content.replace("{{COUNTRY_NAME}}", config["country_name"])
        page_content = page_content.replace("{{CASINO_CARDS}}", cards_html)
        
        # עמוד בריטניה נבנה ישירות כדף הבית הראשי בשורש השרת
        if code == "uk":
            output_file_path = os.path.join(OUTPUT_DIR, "index.html")
        else:
            # שאר המדינות נשמרות בתתי-תיקיות (public/de/index.html)
            country_dir = os.path.join(OUTPUT_DIR, code)
            if not os.path.exists(country_dir):
                os.makedirs(country_dir)
            output_file_path = os.path.join(country_dir, "index.html")
            
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(page_content)
            
    print("✅ Success: Static layout built successfully with SlotMetric TOP 10 Logic.")

if __name__ == "__main__":
    main()
