import os
import json

TEMPLATE_PATH = "templates/index.html"
OUTPUT_DIR = "public"

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
        "meta_description": "Lista oficial de casinos con licencia de la DGOJ in España. Verificación en tiempo real, datos de RTP, métodos de pago y bonos en SlotMetric."
    }
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
         
        # חילוץ קוד האייקון הוקטורי מתוך ה-JSON
        icon_code = casino.get("logo_url", "fa-dice")
        if not str(icon_code).startswith("fa-"):
            icon_code = "fa-dice" # הגנה ורשת ביטחון
    
        logo_html = f'<i class="fa-solid {icon_code} casino-icon-style"></i>'
    
        target_url = casino.get("affiliate_url") or casino.get("official_url") or "#"
        
        card_class = "casino-card featured" if is_featured else "casino-card"
        badge_html = '<span class="sponsored-tag">★ Sponsored TOP</span>' if is_featured else f'<span class="score-tag">Rating: {casino["calculated_score"]}/10</span>'
        rel_tag = 'rel="sponsored nofollow"' if is_featured else 'rel="nofollow noreferrer"'
        
        card = f"""
        <div class="{card_class}">
            <div>
                <div class="logo-container">
                    <i class="fa-solid {icon_code} casino-icon-style"></i>
                    <div class="casino-title-style">{casino['brand_name']}</div>
                </div>
                <div class="card-header">
                    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                        <span class="license-badge">License: #{casino['license_number']}</span>
                        {badge_html}
                    </div>
                </div>
                <div class="features-box">
                    <div class="feature-item"><span>Welcome Bonus:</span> <strong>{bonus}</strong></div>
                    <div class="features-item"><span>Average RTP:</span> <strong>{rtp}</strong></div>
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
            
    print("✅ Success: Static layout built successfully with SlotMetric Vector Icon Integration.")

if __name__ == "__main__":
    main()
