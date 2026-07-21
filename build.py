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

# הלוגואים הגרפיים מוזרקים ישירות כקוד HTML/SVG - אין צורך בקבצים בתיקייה!
EMBEDDED_LOGOS = {
    "duelz": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#1a237e' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='20' fill='#ff9100' text-anchor='middle' dominant-baseline='middle'>DUELZ</text></svg>",
    "bet365": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#005A36' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#FFDF00' text-anchor='middle' dominant-baseline='middle'>bet365</text></svg>",
    "allbritish": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#ffffff' rx='6' stroke='#cf142b' stroke-width='2'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#00247d' text-anchor='middle' dominant-baseline='middle'>ALL BRITISH</text></svg>",
    "playojo": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#4a148c' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='20' fill='#00e676' text-anchor='middle' dominant-baseline='middle'>PlayOJO</text></svg>",
    "rizk": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#000000' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='24' fill='#ffeb3b' text-anchor='middle' dominant-baseline='middle'>RIZK</text></svg>",
    "casimba": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#111111' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>CASIMBA</text></svg>",
    "888casino": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#222222' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#8dfc00' text-anchor='middle' dominant-baseline='middle'>888casino</text></svg>",
    "mrgreen": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#004d40' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='16' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>mr green</text></svg>",
    "grosvenor": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#001834' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>GROSVENOR</text></svg>",
    "leovegas": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#f57c00' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>LeoVegas</text></svg>"
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
        
        # מחלצים את המפתח של הלוגו מתוך כתובת ה-URL שב-JSON
        logo_key = casino.get("logo_url", "").split("/")[-1].replace(".png", "").lower()
        
        # הזרקת קוד ה-SVG ישירות ל-HTML בצורה מאובטחת
        if logo_key in EMBEDDED_LOGOS:
            logo_html = EMBEDDED_LOGOS[logo_key]
        else:
            logo_html = f'<div style="font-weight:bold; color:#1a237e; font-size:1.1rem; padding: 10px; border: 1px solid #ccc; border-radius: 6px; text-align: center;">{casino["brand_name"]}</div>'
            
        card_class = "casino-card featured" if is_featured else "casino-card"
        badge_html = '<span class="sponsored-tag">★ Sponsored TOP</span>' if is_featured else f'<span class="score-tag">Rating: {casino.get("calculated_score", 8.5)}/10</span>'
        
        card = f"""
        <div class="{card_class}">
            <div>
                <div class="logo-container" style="display: flex; align-items: center; justify-content: center; height: 50px; max-width: 160px; margin: 0 auto 15px auto;">
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
    print("✅ Success: Inline SVGs generated perfectly.")

if __name__ == "__main__": main()
