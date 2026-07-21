# ==========================================
# PART 1: CONFIGURATION & ENVIRONMENT SETUP
# ==========================================
import os
import urllib.request
import json

# מילון הלוגואים המעודכן מהתיקייה שהעלית ב-GitHub
LOGOS_CONFIG = {
    "bet365": "https://github.io",
    "LeoVegas": "https://github.io",
    "Unibet": "https://github.io",
    "888": "https://github.io"
}

def init_environment():
    """יצירת התיקיות הנדרשות לבניית הפרויקט בתוך תיקיית public"""
    directories = ["public", "public/assets", "public/assets/logos"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 נוצרה תיקייה: {directory}")

def fetch_resource(name, url, target_dir="public/assets/logos"):
    """פונקציה להורדת הלוגואים בצורה בטוחה"""
    ext = url.split('.')[-1]
    filepath = os.path.join(target_dir, f"{name}.{ext}")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            data = response.read()
            with open(filepath, 'wb') as f:
                f.write(data)
        print(f"✅ הלוגו {name} סונכרן בהצלחה.")
        return filepath
    except Exception as e:
        print(f"❌ שגיאה בהורדת הלוגו {name}: {e}")
        return None
# ==========================================
# PART 2: CORE PROCESS & CASINO CARDS INJECTION
# ==========================================

def generate_casino_cards_html():
    """מייצר את קוד ה-HTML עבור כרטיסיות הקזינו עם הלוגואים החדשים"""
    cards_html = ""
    
    # בניית מבנה כרטיסיות מעוצב לכל מותג שהעלית
    for brand in LOGOS_CONFIG.keys():
        # התאמת נתיב הלוגו המקומי שנוצר בתיקיית public
        logo_path = f"assets/logos/{brand}.png"
        
        cards_html += f"""
        <div class="casino-card" style="border: 1px solid #ddd; padding: 20px; margin: 10px; border-radius: 8px; display: inline-block; background: #fff; text-align: center; width: 200px;">
            <img src="{logo_path}" alt="{brand} logo" style="max-width: 150px; max-height: 60px; object-fit: contain; margin-bottom: 10px;">
            <h3 style="margin: 5px 0; color: #333; text-transform: capitalize;">{brand}</h3>
        </div>
        """
    return cards_html

def build_project():
    """הפונקציה המרכזית שמנהלת את תהליך הבנייה והזרקת הנתונים לאתר"""
    print("🏗️ מתחיל בתהליך הבנייה וההרכבה של האתר...")
    
    # 1. אתחול סביבת העבודה ותיקיית public
    init_environment()
    
    # 2. לולאת הורדה וסנכרון של הלוגואים החדשים שלך
    print("\n🔄 מסנכרן את הלוגואים מהשרת הראשי שלך...")
    for brand_name, logo_url in LOGOS_CONFIG.items():
        fetch_resource(brand_name, logo_url)
        
    # 3. בנייה והזרקת נתונים לתוך קובץ ה-index.html
    print("\n📊 מעבד את תבנית האתר ומזריק את הכרטיסיות...")
    template_path = "templates/index.html"
    output_html_path = "public/index.html"
    
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # יצירת ה-HTML של הכרטיסיות באופן דינמי
            casino_cards_content = generate_casino_cards_html()
            
            # החלפת מחזיקי המקום (Placeholders) בתוכן האמיתי
            html_content = html_content.replace("{{COUNTRY_NAME}}", "Global Market")
            html_content = html_content.replace("{{CASINO_CARDS}}", casino_cards_content)
            
            with open(output_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("✅ קובץ index.html נוצר והוזרק בהצלחה בתוך תיקיית public!")
        except Exception as e:
            print(f"❌ שגיאה בעיבוד קובץ ה-HTML: {e}")
    else:
        print("⚠️ אזהרה: קובץ templates/index.html לא נמצא! אנא ודא שהנתיב תקין.")
    
    print("\n🎉 תהליך הבנייה הסתיים בהצלחה מלאה!")

if __name__ == "__main__":
    build_project()
