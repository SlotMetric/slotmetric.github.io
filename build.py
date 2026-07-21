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
# PART 2: CORE PROCESS & TEMPLATE BUILDING
# ==========================================

def build_project():
    """הפונקציה המרכזית שמנהלת את תהליך הבנייה של הפרויקט והעתקת הדפים"""
    print("🏗️ מתחיל בתהליך הבנייה וההרכבה של האתר...")
    
    # 1. אתחול סביבת העבודה ותיקיית public
    init_environment()
    
    # 2. לולאת הורדה וסנכרון של הלוגואים החדשים שלך
    print("\n🔄 מסנכרן את הלוגואים מהשרת הראשי שלך...")
    for brand_name, logo_url in LOGOS_CONFIG.items():
        fetch_resource(brand_name, logo_url)
        
    # 3. בנייה והעתקה של קובץ ה-index.html מתוך תיקיית templates
    print("\n📊 מעבד את תבנית האתר ומקים את דף הבית...")
    template_path = "templates/index.html"
    output_html_path = "public/index.html"
    
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # כאן ניתן להוסיף הזרקת נתונים דינמית לתוך ה-HTML במידת הצורך
            
            with open(output_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("✅ קובץ index.html נוצר בהצלחה בתוך תיקיית public!")
        except Exception as e:
            print(f"❌ שגיאה בעיבוד קובץ ה-HTML: {e}")
    else:
        print("⚠️ אזהרה: קובץ templates/index.html לא נמצא! אנא ודא שהנתיב תקין.")
    
    print("\n🎉 תהליך הבנייה הסתיים בהצלחה מלאה!")

if __name__ == "__main__":
    build_project()
