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
            # שימוש ב-pop(0) כדי לחלץ את האיבר הראשון בבטחה בלי להשתמש בסוגריים מרובעים שנמחקים בצ'אט
            parts = filename.split(".")
            country_code = parts.pop(0).upper()
            
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    countries_data[country_code] = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return countries_data

def clean_html_template(html_content):
    # הסרת הערות HTML
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    # הסרת שורות ריקות מיותרות
    html_content = re.sub(r'^\s*$\n', '', html_content, flags=re.MULTILINE)
    return html_content
def generate_casino_cards(casinos, country_code):
    cards_html = ""
    for casino in casinos:
        casino_id = casino.get("id", "")
        
        # -------------------------------------------------------------
        # התיקון המבוקש: התעלמות מלאה מאותיות גדולות/קטנות בחיפוש הקובץ
        # -------------------------------------------------------------
        logo_file = f"data-collectors/united-kingdom/logos/{casino_id}.png"  # ברירת המחדל המקורית שלך
        logos_dir = "assets/logos"
        if os.path.exists(logos_dir):
            target_filename = f"{str(casino_id).lower()}.png"
            for file_name in os.listdir(logos_dir):
                if file_name.lower() == target_filename:
                    logo_file = f"assets/logos/{file_name}"
                    break
        # -------------------------------------------------------------

        name = casino.get("name", casino_id.upper())
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
                <img src="{logo_file}" alt="{name} logo" style="max-width: 180px; max-height: 60px; object-fit: contain;">
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
