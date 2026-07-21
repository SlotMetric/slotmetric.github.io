import os
import json

TEMPLATE_PATH = "templates/index.html"
OUTPUT_DIR = "public"
# תיקיית המקור שבה העלית את הלוגואים האמיתיים
REPO_LOGOS_DIR = os.path.join("assets", "logos")
# תיקיית היעד הציבורית שהאתר קורא ממנה
PUBLIC_LOGOS_DIR = os.path.join(OUTPUT_DIR, "assets", "logos")

COUNTRIES_CONFIG = {
    "uk": {"country_name": "United Kingdom", "data_file": "processed-data/uk-casinos.json"},
    "de": {"country_name": "Germany (Deutschland)", "data_file": "processed-data/germany-casinos.json"},
    "nl": {"country_name": "Netherlands (Nederland)", "data_file": "processed-data/netherlands-casinos.json"},
    "se": {"country_name": "Sweden (Sverige)", "data_file": "processed-data/sweden-casinos.json"},
    "es": {"country_name": "Spain (España)", "data_file": "processed-data/spain-casinos.json"}
}

def get_existing_logo_file(brand_key):
    """בודק איזה קובץ לוגו אמיתי קיים בתיקיית הנכסים (PNG או SVG)"""
    for ext in [".png", ".svg", ".jpg", ".jpeg"]:
        filename = f"{brand_key}{ext}"
        if os.path.exists(os.path.join(REPO_LOGOS_DIR, filename)):
            return filename
    return None

def load_template():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<html><body><h1>{{COUNTRY_NAME}}</h1><div>{{CASINO_CARDS}}</div></body></html>"

def build_casino_cards(json_path, is_subfolder):
    if not os.path.exists(json_path): return "<!-- No data -->"
    with open(json_path, "r", encoding="utf-8") as f: casinos = json.load(f)
    
    all_clicks = [int(c.get("user_clicks", 10)) for c in casinos]
    max_clicks = max(all_clicks) if all_clicks else 100
    
    featured_casinos = [c for c in casinos if c.get("is_featured") == True]
    regular_casinos = [c for c in casinos if not c.get("is_featured") == True]
    
    for casino in regular_casinos:
        clicks = int(casino.get("user_clicks", 50))
        casino["calculated_score"] = round(7.5 + ((clicks / max_clicks) * 2.1), 1)
        
    regular_casinos.sort(key=lambda x: x.get("calculated_score", 8.5), reverse=True)
    final_list = featured_casinos[:2] + regular_casinos[:(10 - len(featured_casinos[:2]))]
    
    cards_html = []
    for casino in final_list:
        is_featured = casino.get("is_featured") == True
        features = casino.get("features", {})
        
        # חילוץ מפתח נקי של המותג (למשל 'bet365')
        brand_key = casino.get("brand_name", "").lower().replace(" ", "").replace("casino", "")
        
        # חיפוש קובץ הלוגו האמיתי שהעלית לתיקייה
        logo_filename = get_existing_logo_file(brand_key)
        
        if logo_filename:
            # העתקת הקובץ לתיקיית האתר הציבורית בזמן ה-Build
            os.makedirs(PUBLIC_LOGOS_DIR, exist_ok=True)
            import shutil
            shutil.copy(os.path.join(REPO_LOGOS_DIR, logo_filename), os.path.join(PUBLIC_LOGOS_DIR, logo_filename))
            
            # יצירת תגית התמונה עבור הלוגו המקורי
            path_prefix = "../" if is_subfolder else ""
            final_src = f"{path_prefix}assets/logos/{logo_filename}"
            logo_html = f'<img src="{final_src}" alt="{casino["brand_name"]}" style="max-height: 50px; max-width: 150px; object-fit: contain; display: block; margin: 0 auto;">'
        else:
            # גיבוי טקסט אלגנטי רק אם שכחת להעלות קובץ עבור קזינו מסוים
            logo_html = f'<div style="font-family:\'Montserrat\',sans-serif; font-weight:700; color:#455a64; font-size:1.2rem; text-align:center;">{casino["brand_name"]}</div>'
            
        card_class = "casino-card featured" if is_featured else "casino-card"
        badge_html = '<span class="sponsored-tag">★ Sponsored TOP</span>' if is_featured else f'<span class="score-tag">Rating: {casino.get("calculated_score", 8.5)}/10</span>'
        
        card = f"""
        <div class="{card_class}">
            <div>
                <div class="logo-container" style="display: flex; align-items: center; justify-content: center; height: 50px; width: 100%; max-width: 160px; margin: 0 auto 15px auto;">
                    {logo_html}
                </div>
                <div class="card-header">
                    <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                        <span class="license-badge">License: #{casino['license_number']}</span>
                        {badge_html}
                    </div>
                </div>
                <div class="features-box">
                    <div class="feature-item"><span>Welcome Bonus:</span> <strong>{features.get("bonus_text", "N/A")}</strong></div>
                    <div class="feature-item"><span>Average RTP:</span> <strong>{features.get("average_rtp", "N/A")}</strong></div>
                    <div class="feature-item"><span>Min Deposit:</span> <strong>{features.get("min_deposit", "N/A")}</strong></div>
                    <div class="feature-item"><span>Payments:</span> <strong style="font-size:0.8rem; max-width:60%; color:#455a64;">{features.get("payment_methods", "N/A")}</strong></div>
                    <div class="feature-item"><span>Crypto Support:</span> <strong class="crypto-no">❌ No (Fiat)</strong></div>
                </div>
            </div>
            <a href="{casino.get("affiliate_url") or casino.get("official_url", "#")}" class="btn-play" rel="nofollow" target="_blank">Verify & Play</a>
        </div>
        """
        cards_html.append(card)
    return "\n".join(cards_html)

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    template = load_template()
    
    for code, config in COUNTRIES_CONFIG.items():
        is_subfolder = (code != "uk")
        cards_html = build_casino_cards(config["data_file"], is_subfolder)
        
        page_content = template.replace("{{COUNTRY_NAME}}", config["country_name"]).replace("{{CASINO_CARDS}}", cards_html)
        page_content = page_content.replace("{{PAGE_TITLE}}", "SlotMetric Database").replace("{{LANG_CODE}}", "en").replace("{{COUNTRY_CODE}}", code)
        
        output_file_path = os.path.join(OUTPUT_DIR, "index.html") if code == "uk" else os.path.join(OUTPUT_DIR, code, "index.html")
        if is_subfolder and not os.path.exists(os.path.dirname(output_file_path)): os.makedirs(os.path.dirname(output_file_path))
        
        with open(output_file_path, "w", encoding="utf-8") as f: f.write(page_content)
    print("✅ Success: Built perfectly using uploaded local files.")

if __name__ == "__main__": main()
