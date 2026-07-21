import os
import json

TEMPLATE_PATH = "templates/index.html"
OUTPUT_DIR = "public"

COUNTRIES_CONFIG = {
    "uk": {"country_name": "United Kingdom", "data_file": "processed-data/uk-casinos.json"},
    "de": {"country_name": "Germany (Deutschland)", "data_file": "processed-data/germany-casinos.json"},
    "nl": {"country_name": "Netherlands (Nederland)", "data_file": "processed-data/netherlands-casinos.json"},
    "se": {"country_name": "Sweden (Sverige)", "data_file": "processed-data/sweden-casinos.json"},
    "es": {"country_name": "Spain (España)", "data_file": "processed-data/spain-casinos.json"}
}

# קישורים ישירים לציורי לוגו רשמיים ופתוחים באינטרנט (עוקף את התיקייה הריקה)
REAL_ONLINE_LOGOS = {
    "bet365": "https://logo.dev", # קישור גרפי ישיר
    "888casino": "https://logo.dev",
    "mrgreen": "https://logo.dev",
    "leovegas": "https://logo.dev",
    "playojo": "https://logo.dev",
    "rizk": "https://logo.dev",
    "duelz": "https://logo.dev",
    "casimba": "https://logo.dev"
}

def load_template():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<html><body><h1>{{COUNTRY_NAME}}</h1><div>{{CASINO_CARDS}}</div></body></html>"

def build_casino_cards(json_path):
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
        
        brand_lower = casino.get("brand_name", "").lower().replace(" ", "")
        url_lower = casino.get("logo_url", "").lower()
        
        # מחפשים אם יש לנו קישור תמונה מוכן ברשת עבור המותג הזה
        logo_src = None
        for key, online_url in REAL_ONLINE_LOGOS.items():
            if (key in brand_lower) or (key in url_lower):
                logo_src = online_url
                break
                
        # אם מצאנו קישור לציור אמיתי, נציג אותו, אחרת נציג כותרת נקייה
        if logo_src:
            logo_html = f'<img src="{logo_src}" alt="{casino["brand_name"]}" style="height: 40px; max-width: 140px; object-fit: contain; display: block; margin: 0 auto;">'
        else:
            logo_html = f'<div style="font-family:\'Montserrat\',sans-serif; font-weight:800; color:#1a237e; font-size:1.2rem; text-transform:uppercase; text-align:center; width:100%;">{casino["brand_name"]}</div>'
            
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
        cards_html = build_casino_cards(config["data_file"])
        
        page_content = template.replace("{{COUNTRY_NAME}}", config["country_name"]).replace("{{CASINO_CARDS}}", cards_html)
        page_content = page_content.replace("{{PAGE_TITLE}}", "SlotMetric Database").replace("{{LANG_CODE}}", "en").replace("{{COUNTRY_CODE}}", code)
        
        output_file_path = os.path.join(OUTPUT_DIR, "index.html") if code == "uk" else os.path.join(OUTPUT_DIR, code, "index.html")
        if (code != "uk") and not os.path.exists(os.path.dirname(output_file_path)): os.makedirs(os.path.dirname(output_file_path))
        
        with open(output_file_path, "w", encoding="utf-8") as f: f.write(page_content)
    print("✅ Success: Built with live web images.")

if __name__ == "__main__": main()
