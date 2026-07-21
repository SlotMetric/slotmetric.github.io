import os
import json
import re

def load_processed_data():
    countries_data = {}
    data_dir = "processed-data"
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found.")
        return countries_data

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            # ה- המקורי והחיוני שלך הוחזר למקומו בדיוק!
            country_code = filename.split(".")[0].upper()
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    countries_data[country_code] = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return countries_data

def clean_html_template(html_content):
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'^\s*$\n', '', html_content, flags=re.MULTILINE)
    return html_content

def extract_clean_keys(casino):
    search_keys = []
    brand = casino.get("brand_name", "").lower().replace(" ", "")
    if brand:
        search_keys.append(brand)
    
    affiliate_url = casino.get("affiliate_link", "").lower()
    if affiliate_url:
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', affiliate_url)
        if domain_match:
            full_domain = domain_match.group(1)
            search_keys.append(full_domain)
            domain_parts = full_domain.split('.')
            if len(domain_parts) > 1:
                search_keys.append(domain_parts[0])
                search_keys.append(domain_parts[1])
                
    casino_id = casino.get("id", "").lower().replace(" ", "")
    if casino_id:
        search_keys.append(casino_id)
        
    return list(set(search_keys))

# מילון ה-SVG המקורי שלך - הוספתי לו את המפתח "uk-38790" שראינו עכשיו ב-JSON שלך!
EMBEDDED_LOGOS = {
    "bet365": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#005A36' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#FFDF00' text-anchor='middle' dominant-baseline='middle'>bet365</text></svg>",
    "duelz": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#1a237e' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='20' fill='#ff9100' text-anchor='middle' dominant-baseline='middle'>DUELZ</text></svg>",
    "british": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#ffffff' rx='6' stroke='#cf142b' stroke-width='2'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#00247d' text-anchor='middle' dominant-baseline='middle'>ALL BRITISH</text></svg>",
    "uk-38790": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#ffffff' rx='6' stroke='#cf142b' stroke-width='2'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#00247d' text-anchor='middle' dominant-baseline='middle'>ALL BRITISH</text></svg>",
    "playojo": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#4a148c' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='20' fill='#00e676' text-anchor='middle' dominant-baseline='middle'>PlayOJO</text></svg>",
    "rizk": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#000000' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='24' fill='#ffeb3b' text-anchor='middle' dominant-baseline='middle'>RIZK</text></svg>",
    "casimba": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#111111' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>CASIMBA</text></svg>",
    "888": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#222222' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#8dfc00' text-anchor='middle' dominant-baseline='middle'>888casino</text></svg>",
    "mrgreen": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#004d40' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='16' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>mr green</text></svg>",
    "grosvenor": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#001834' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='14' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>GROSVENOR</text></svg>",
    "leovegas": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#f57c00' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>LeoVegas</text></svg>",
    "tipico": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#ff0000' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>Tipico</text></svg>",
    "bwin": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#000000' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='24' fill='#fdd835' text-anchor='middle' dominant-baseline='middle'>bwin</text></svg>",
    "wildz": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#4a00e0' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='22' fill='#ff007f' text-anchor='middle' dominant-baseline='middle'>WILDZ</text></svg>",
    "wunderino": "<svg xmlns='http://w3.org' viewBox='0 0 160 50' style='width:100%; height:100%;'><rect width='100%' height='100%' fill='#00bcd4' rx='6'/><text x='50%' y='55%' font-family='sans-serif' font-weight='bold' font-size='18' fill='#ffffff' text-anchor='middle' dominant-baseline='middle'>Wunderino</text></svg>"
}
def generate_casino_cards(casinos, country_code):
    cards_html = ""
    for casino in casinos:
        casino_id = casino.get("id", "")
        search_keys = extract_clean_keys(casino)
        
        logo_html = ""
        for key, svg_code in EMBEDDED_LOGOS.items():
            if any(key in k for k in search_keys):
                logo_html = svg_code
                break

        if not logo_html:
            # שימוש במנגנון המקורי והחסין שלכם שמציל את הולנד ושומר על השמות והצבעים
            logo_html = f'<div style="font-family:\'Montserrat\',sans-serif; font-weight:800; color:#fff; font-size:1.2rem; text-transform:uppercase; text-align:center; width:100%; padding:12px; border-radius:8px; background:{casino.get("color", "#212529")};">{casino.get("brand_name", casino_id.upper())}</div>'

        rating = casino.get("rating", "N/A")
        bonus = casino.get("bonus", "No Welcome Bonus Available")
        license_val = casino.get("license", "N/A")
        rtp = casino.get("rtp", "N/A")
        min_deposit = casino.get("min_deposit", "N/A")
        
        payments_list = casino.get("payments", [])
        payments_str = ", ".join(payments_list) if payments_list else "N/A"
        
        crypto_val = casino.get("crypto", "No")
        crypto_str = "Yes (Crypto)" if crypto_val == "Yes" else "X No (Fiat)"
        crypto_color = "#2f855a" if crypto_val == "Yes" else "#e53e3e"

        cards_html += f"""
        <div class="casino-card" style="border: 2px solid #eef2f5; padding: 25px; margin: 15px; border-radius: 12px; display: inline-block; background: #fff; text-align: left; width: 280px; box-shadow: 0 8px 16px rgba(0,0,0,0.04); vertical-align: top;">
            <div style="text-align: center; height: 70px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                {logo_html}
            </div>
            <div style="border-top: 1px solid #f1f4f6; padding-top: 10px; font-family: sans-serif; font-size: 13px; color: #4a5568;">
                <p><strong>License:</strong> {license_val}</p>
                <p><strong>Rating:</strong> <span style="color: #2b6cb0; font-weight: bold;">{rating}/10</span></p>
                <p><strong>Welcome Bonus:</strong> <span style="color: #2f855a; font-weight: bold;">{bonus}</span></p>
                <p><strong>Average RTP:</strong> {rtp}</p>
                <p><strong>Min Deposit:</strong> {min_deposit}</p>
                <p><strong>Payments:</strong> <span style="font-size: 11px;">{payments_str}</span></p>
                <p><strong>Crypto Support:</strong> <span style="color: {crypto_color}; font-weight: bold;">{crypto_str}</span></p>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <a href="#" style="background: #00e676; color: #fff; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; font-family: sans-serif; box-shadow: 0 4px 10px rgba(0,230,118,0.3);">Verify & Play</a>
            </div>
        </div>
        """
    return cards_html

def build():
    countries_data = load_processed_data()
    
    template_path = "templates/index.html"
    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found.")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    os.makedirs("public", exist_ok=True)

    for country_code, casinos in countries_data.items():
        country_name = country_code.replace("-", " ").title()
        cards_html = generate_casino_cards(casinos, country_code)
        
        page_content = template_content.replace("{{COUNTRY_NAME}}", country_name)
        page_content = page_content.replace("{{CASINO_CARDS}}", cards_html)
        page_content = clean_html_template(page_content)
        
        if country_code == "UNITED-KINGDOM":
            output_path = "public/index.html"
        else:
            country_dir = os.path.join("public", country_code.lower())
            os.makedirs(country_dir, exist_ok=True)
            output_path = os.path.join(country_dir, "index.html")
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_content)
            
        print(f"Successfully generated page for {country_name} -> {output_path}")

if __name__ == "__main__":
    build()
