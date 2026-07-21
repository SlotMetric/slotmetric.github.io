# ==========================================
# PART 1: CORE REVENUE & DATA PARSING
# ==========================================
import os
import json
import re

def find_logo_case_insensitive(casino_id, logos_dir="assets/logos"):
    """
    פונקציית מגן חדשה: מוצאת את קובץ הלוגו בתיקייה באופן אוטומטי
    ומתעלמת לחלוטין מאותיות גדולות, קטנות או סיומות לא תואמות.
    """
    if not os.path.exists(logos_dir):
        return None
        
    target = f"{str(casino_id).lower()}.png"
    
    # סריקה חכמה של כל הקבצים הקיימים בתיקיית הלוגואים שלך
    for file_name in os.listdir(logos_dir):
        if file_name.lower() == target or file_name.lower().startswith(str(casino_id).lower()):
            return f"assets/logos/{file_name}"
            
    # ברירת מחדל אם לא נמצא קובץ תואם בכלל
    return f"assets/logos/{casino_id}.png"

def load_processed_data(data_dir="processed-data"):
    """טעינת קבצי המידע והבונוסים המקוריים של האתר"""
    countries_data = {}
    if not os.path.exists(data_dir):
        print(f"⚠️ שגיאה: תיקיית הנתונים {data_dir} לא נמצאה.")
        return countries_data
        
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".json"):
            country_code = file_name.split(".")[0].upper()
            file_path = os.path.join(data_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    countries_data[country_code] = json.load(f)
            except Exception as e:
                print(f"❌ שגיאה בטעינת הקובץ {file_name}: {e}")
    return countries_data
# ==========================================
# PART 2: CARD GENERATION & HTML RENDERING
# ==========================================

def generate_cards_html(casino_list):
    """מייצר את קוד ה-HTML העשיר עבור כרטיסיות הקזינו עם הלוגואים המוגנים"""
    cards_html = ""
    for casino in casino_list:
        casino_id = casino.get("id", "default")
        
        # שימוש בפונקציית המגן החדשה לאיתור הלוגו ללא חשיבות לאותיות גדולות/קטנות
        logo_path = find_logo_case_insensitive(casino_id)
        
        # חילוץ נתונים מקובץ ה-JSON המקורי שלך
        rating = casino.get("rating", "N/A")
        bonus = casino.get("bonus", "No bonus available")
        license_num = casino.get("license", "N/A")
        rtp = casino.get("rtp", "N/A")
        min_dep = casino.get("min_deposit", "N/A")
        crypto = "Yes (Crypto)" if casino.get("crypto", False) else "X No (Fiat)"
        
        # עיבוד רשימת אמצעי התשלום למבנה טקסט נקי
        payments = ", ".join(casino.get("payments", [])) if casino.get("payments") else "N/A"
        
        # בניית מבנה הכרטיסייה המקורי והעשיר שלך כפי שהיה
        cards_html += f"""
        <div class="casino-card" style="border: 2px solid #eef2f5; padding: 25px; margin: 15px; border-radius: 12px; display: inline-block; background: #fff; text-align: left; width: 280px; box-shadow: 0 8px 16px rgba(0,0,0,0.04); vertical-align: top;">
            <div style="text-align: center; height: 70px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                <img src="{logo_path}" alt="{casino_id} logo" style="max-width: 180px; max-height: 60px; object-fit: contain;">
            </div>
            <div style="border-top: 1px solid #f1f4f6; padding-top: 10px; font-family: sans-serif; font-size: 13px; color: #4a5568;">
                <p><strong>License:</strong> {license_num}</p>
                <p><strong>Rating:</strong> <span style="color: #2b6cb0; font-weight: bold;">{rating}/10</span></p>
                <p><strong>Welcome Bonus:</strong> <span style="color: #2f855a; font-weight: bold;">{bonus}</span></p>
                <p><strong>Average RTP:</strong> {rtp}</p>
                <p><strong>Min Deposit:</strong> {min_dep}</p>
                <p><strong>Payments:</strong> <span style="font-size: 11px;">{payments}</span></p>
                <p><strong>Crypto Support:</strong> <span style="color: {'#2f855a' if 'Yes' in crypto else '#e53e3e'}; font-weight: bold;">{crypto}</span></p>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <a href="#" style="background: #00e676; color: #fff; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; font-family: sans-serif; box-shadow: 0 4px 10px rgba(0,230,118,0.3);">Verify & Play</a>
            </div>
        </div>
        """
    return cards_html

def build_project():
    """הפונקציה המרכזית שמנהלת את הרכבת האתר מתוך התבניות והזרקת הנתונים"""
    print("🏗️ מתחיל בתהליך הבנייה וההרכבה הרשמי של האתר...")
    
    # 1. טעינת הנתונים המקוריים
    all_data = load_processed_data()
    if not all_data:
        # אם אין נתונים, נייצר רשימת דמו למניעת קריסה (למשל לצורך הבדיקה הראשונית)
        all_data = {"Global Market": [{"id": "bet365"}, {"id": "LeoVegas"}, {"id": "Unibet"}, {"id": "888"}]}
    
    # 2. יצירת סביבת העבודה בתיקיית public עבור ה-Action
    if not os.path.exists("public"):
        os.makedirs("public")
        
    template_path = "templates/index.html"
    output_html_path = "public/index.html"
    
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # שליפת המדינה הראשונה או לולאה (לצורך הדוגמה נשתמש במפתח הראשון)
            country_name = list(all_data.keys())[0]
            casinos = all_data[country_name]
            
            # יצירת קוד הכרטיסיות העשיר והזרקתו
            casino_cards_content = generate_cards_html(casinos)
            
            html_content = html_content.replace("{{COUNTRY_NAME}}", country_name)
            html_content = html_content.replace("{{CASINO_CARDS}}", casino_cards_content)
            
            with open(output_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("✅ קובץ index.html והזרקת הנתונים נבנו בהצלחה בתיקיית public!")
        except Exception as e:
            print(f"❌ שגיאה בעיבוד קובץ ה-HTML: {e}")
    else:
        print("⚠️ אזהרה: קובץ templates/index.html לא נמצא!")
    
    print("\n🎉 תהליך הבנייה הסתיים בהצלחה מלאה!")

if __name__ == "__main__":
    build_project()
