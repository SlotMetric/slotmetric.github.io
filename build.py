import os
import json

TEMPLATE_PATH = "templates/index.html"
OUTPUT_DIR = "public"
LOGOS_DIR = "public/assets/logos"

COUNTRIES_CONFIG = {
    "uk": {
        "country_name": "United Kingdom",
        "data_file": "processed-data/uk-casinos.json",
        "page_title": "Verified Licensed Casinos in the UK | SlotMetric",
        "meta_description": "Check the official list of UKGC licensed online casinos. Real-time data verification, licensing numbers, and features on SlotMetric."
    },
    "de": {
        "country_name": "Germany (Deutschland)",
        "data_file": "processed-data/germany-casinos.json",
        "page_title": "Erlaubte Online Casinos in Deutschland | SlotMetric",
        "meta_description": "Offizielle Whitelist der GGL für Online Casinos in Deutschland. Überprüfte Lizenzen, RTP-Werte und Bonus-Metriken auf SlotMetric."
    },
    "nl": {
        "country_name": "Netherlands (Nederland)",
        "data_file": "processed-data/netherlands-casinos.json",
        "page_title": "Legale Online Casino's in Nederland | SlotMetric",
        "meta_description": "Bekijk de officiële Ksa kansspelvergunninghouders. Betrouwbare online casino's, live RTP-data und bonussen op SlotMetric."
    },
    "se": {
        "country_name": "Sweden (Sverige)",
        "data_file": "processed-data/sweden-casinos.json",
        "page_title": "Licensierade Online Casinon i Sverige | SlotMetric",
        "meta_description": "Officiell lista över casinon med svensk licens från Spelinspektionen. Verifierade spellicenser, RTP-data och bonusar auf SlotMetric."
    },
    "es": {
        "country_name": "Spain (España)",
        "data_file": "processed-data/spain-casinos.json",
        "page_title": "Casinos Online Autorizados en España | SlotMetric",
        "meta_description": "Lista oficial de casinos con licencia de la DGOJ en España. Verificación en tiempo real, datos de RTP, métodos de pago y bonos en SlotMetric."
    }
}

# מאגר קודים גרפיים רשמיים של המותגים (ייוצרו כקבצים פיזיים יציבים בשרת בתוך תיקיית האתר)
EMBEDDED_LOGOS = {
    "duelz": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#1a237e' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='20' fill='#ff9100' text-anchor='middle' dominant-baseline='middle'>DUELZ</text></svg>",
    "bet365": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#005A36' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#FFDF00' text-anchor='middle' dominant-baseline='middle'>bet365</text></svg>",
    "allbritish": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#ffffff' rx='6' stroke='#cf142b' stroke-width='2'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#00247d' text-anchor='middle' dominant-baseline='middle'>ALL BRITISH</text></svg>",
    "playojo": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#4a148c' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='20' fill='#00e676' text-anchor='middle' dominant-baseline='middle'>PlayOJO</text></svg>",
    "rizk": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#000000' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='24' fill='#ffeb3b' text-anchor='middle' dominant-baseline='middle'>RIZK</text></svg>",
    "casimba": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#111111' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>CASIMBA</text></svg>",
    "888casino": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#222222' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#8dfc00' text-anchor='middle' dominant-baseline='middle'>888casino</text></svg>",
    "mrgreen": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#004d40' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='16' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>mr green</text></svg>",
    "grosvenor": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#001834' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>GROSVENOR</text></svg>",
    "leovegas": "<svg xmlns='http://w3.org' viewBox='0 0 160 50'><rect width='100%' height='100%' fill='#f57c00' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>LeoVegas</text></svg>"
}

def load_template():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"❌ Template file missing at: {TEMPLATE_PATH}")
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def build_casino_cards(json_path):
    if not os.path.exists(json_path):
        print(f"⚠️ Data file not found for: {json_path}.")
        return "<!-- No data available -->"
        
    with open(json_path, "r", encoding="utf-8") as f:
        casinos = json.load(f)
        
    all_clicks = [int(c.get("user_clicks", 10)) for c in casinos]
    max_clicks = max(all_clicks) if all_clicks else 100
    if max_clicks == 0: max_clicks = 100

    for casino in casinos:
        try:
            clicks = int(casino.get("user_clicks", 50))
            calculated_rating = 7.5 + ((clicks / max_clicks) * 2.1)
            casino["calculated_score"] = round(calculated_rating, 1)
            
            if casino["calculated_score"] > 9.8: casino["calculated_score"] = 9.8
            if casino["calculated_score"] < 7.0: casino["calculated_score"] = 7.5
        except Exception:
            casino["calculated_score"] = 8.5
            
    featured_casinos = [c for c in casinos if c.get("is_featured") == True]
    regular_casinos = [c for c in casinos if not c.get("is_featured") == True]
    
    regular_casinos.sort(key=lambda x: x["calculated_score"], reverse=True)
    final_list = featured_casinos[:2] + regular_casinos[:(10 - len(featured_casinos[:2]))]
    
    cards_html = []
    
    for casino in final_list:
        is_featured = casino.get("is_featured") == True
        features = casino.get("features", {})
        
        bonus = features.get("bonus_text") or "Reviewing Bonus Terms"
        rtp = features.get("average_rtp") or "Calculating Metrics"
        min_dep = features.get("min_deposit") or "£10"
        payments = features.get("payment_methods") or "Visa, Mastercard, E-Wallets"
        crypto_supported = features.get("crypto_supported") == True
        
        crypto_html = '<strong class="crypto-yes">✅ Yes</strong>' if crypto_supported else '<strong class="crypto-no">❌ No (Fiat)</strong>'
        
        # בנייה והזרקה של קובצי לוגו פיזיים מקומיים באתר (חסין מפני חוסמי פרסומות ב-100%)
        logo_key = casino.get("logo_url", "").split("/")[-1].replace(".png", "").lower()
        if logo_key in EMBEDDED_LOGOS:
            logo_file_name = f"{logo_key}.svg"
            with open(os.path.join(LOGOS_DIR, logo_file_name), "w", encoding="utf-8") as svg_file:
                svg_file.write(EMBEDDED_LOGOS[logo_key])
            logo_html = f'<img src="/assets/logos/{logo_file_name}" alt="{casino["brand_name"]} logo" class="casino-logo" loading="lazy">'
        else:
            logo_html = f'<div style="font-weight:bold; color:#1a237e; font-size:1.2rem;">{casino["brand_name"]}</div>'
            
        target_url = casino.get("affiliate_url") or casino.get("official_url") or "#"
        
        card_class = "casino-card featured" if is_featured else "casino-card"
        badge_html = '<span class="sponsored-tag">★ Sponsored TOP</span>' if is_featured else f'<span class="score-tag">Rating: {casino["calculated_score"]}/10</span>'
        rel_tag = 'rel="sponsored nofollow"' if is_featured else 'rel="nofollow noreferrer"'
        
        card = f"""
        <div class="{card_class}">
            <div>
                <div class="logo-container">
                    {logo_html}
                </div>
                <div class="card-header">
                    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                        <span class="license-badge">License: #{casino['license_number']}</span>
                        {badge_html}
                    </div>
                </div>
                <div class="features-box">
                    <div class="feature-item"><span>Welcome Bonus:</span> <strong>{bonus}</strong></div>
                    <div class="feature-item"><span>Average RTP:</span> <strong>{rtp}</strong></div>
                    <div class="feature-item"><span>Min Deposit:</span> <strong>{min_dep}</strong></div>
                    <div class="feature-item"><span>Payments:</span> <strong style="font-size: 0.8rem; max-width: 60%; color: #455a64;">{payments}</strong></div>
                    <div class="feature-item"><span>Crypto Support:</span> {crypto_html}</div>
                </div>
            </div>
            <a href="{target_url}" class="btn-play" {rel_tag} target="_blank">Verify & Play</a>
        </div>
        """
        cards_html.append(card)
        
    return "\n".join(cards_html)

def main():
    print("Starting static website build for SlotMetric...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(LOGOS_DIR):
        os.makedirs(LOGOS_DIR)
        
    template = load_template()
    
    for code, config in COUNTRIES_CONFIG.items():
        print(f"📦 Processing country layout for: {config['country_name']} ({code})")
        cards_html = build_casino_cards(config["data_file"])
        
        page_content = template
        page_content = page_content.replace("{{PAGE_TITLE}}", config.get("page_title", "SlotMetric Database"))
        page_content = page_content.replace("{{META_DESCRIPTION}}", config.get("meta_description", ""))
        page_content = page_content.replace("{{LANG_CODE}}", "en")
        page_content = page_content.replace("{{COUNTRY_CODE}}", code)
        page_content = page_content.replace("{{COUNTRY_NAME}}", config["country_name"])
        page_content = page_content.replace("{{CASINO_CARDS}}", cards_html)
        
        if code == "uk":
            output_file_path = os.path.join(OUTPUT_DIR, "index.html")
        else:
            country_dir = os.path.join(OUTPUT_DIR, code)
            if not os.path.exists(country_dir):
                os.makedirs(country_dir)
            output_file_path = os.path.join(country_dir, "index.html")
            
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(page_content)
            
    print("✅ Success: Static layout built successfully with SlotMetric Official Logos.")

if __name__ == "__main__":
    main()
