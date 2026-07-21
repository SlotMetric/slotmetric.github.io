import os
import json
import urllib.request
import shutil
from urllib.parse import urlparse

TEMPLATE_PATH = "templates/index.html"
OUTPUT_DIR = "public"
REPO_LOGOS_DIR = os.path.join("assets", "logos")
PUBLIC_LOGOS_DIR = os.path.join(OUTPUT_DIR, "assets", "logos")

COUNTRIES_CONFIG = {
    "uk": {"country_name": "United Kingdom", "data_file": "processed-data/uk-casinos.json"},
    "de": {"country_name": "Germany (Deutschland)", "data_file": "processed-data/germany-casinos.json"},
    "nl": {"country_name": "Netherlands (Nederland)", "data_file": "processed-data/netherlands-casinos.json"},
    "se": {"country_name": "Sweden (Sverige)", "data_file": "processed-data/sweden-casinos.json"},
    "es": {"country_name": "Spain (España)", "data_file": "processed-data/spain-casinos.json"}
}

BASE_DOWNLOAD_URL = "https://logo.dev{}?token=pk_MXVwY_U6T2mZ9h7v_X_g_A"

def extract_domain(casino):
    """מחלץ את שם הדומיין המדויק מתוך הקישורים שבתוך ה-JSON"""
    for key in ["official_url", "affiliate_url"]:
        url = casino.get(key, "")
        if url and "http" in url:
            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.replace("www.", "")
                if domain:
                    return domain
            except:
                pass
                
    # גיבוי אם אין קישור תקין - נשתמש בשם המותג
    brand = casino.get("brand_name", "").lower().replace(" ", "").replace("casino", "")
    return f"{brand}.com"

def download_logo_if_needed(brand_key, domain_name):
    """מוריד את הלוגו לפי הדומיין האמיתי לתיקיית הריפו ומעתיק ל-public"""
    os.makedirs(REPO_LOGOS_DIR, exist_ok=True)
    os.makedirs(PUBLIC_LOGOS_DIR, exist_ok=True)
    
    filename = f"{brand_key}.png"
    repo_path = os.path.join(REPO_LOGOS_DIR, filename)
    public_path = os.path.join(PUBLIC_LOGOS_DIR, filename)
    
    if not os.path.exists(repo_path):
        print(f"📥 Downloading logo for {brand_key} using domain: {domain_name}...")
        url = BASE_DOWNLOAD_URL.format(domain_name)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response, open(repo_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ Saved to assets/logos/: {filename}")
        except Exception as e:
            print(f"❌ Download failed for {brand_key} ({domain_name}): {e}")
            return None
            
    if os.path.exists(repo_path):
        shutil.copy(repo_path, public_path)
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
        
        # יצירת מפתח שם נקי לקובץ התמונה (למשל 'bet365' או 'allbritish')
        brand_key = casino.get("brand_name", "").lower().replace(" ", "").replace("casino", "")
        
        # חילוץ הדומיין האמיתי לצורך ההורדה (למשל 'allbritishcasino.com')
        domain_name = extract_domain(casino)
        
        logo_filename = download_logo_if_needed(brand_key, domain_name)
        
        if logo_filename:
            path_prefix = "../" if is_subfolder else ""
            final_src = f"{path_prefix}assets/logos/{logo_filename}"
            logo_html = f'<img src="{final_src}" alt="{casino["brand_name"]}" style="max-height: 45px; max-width: 140px; object-fit: contain; display: block; margin: 0 auto;">'
        else:
            logo_html = f'<div style="font-family:\'Montserrat\',sans-serif; font-weight:800; color:#1a237e; font-size:1.1rem; text-transform:uppercase; text-align:center; width:100%;">{casino["brand_name"]}</div>'
            
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
    print("✅ Success: Built and saved logos locally using smart domain extraction.")

if __name__ == "__main__": main()
