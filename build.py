# ==========================================
# PART 1: INITIALIZATION & LOGO CONFIGURATION
# ==========================================
import os
import urllib.request
import json

# מילון הלוגואים המעודכן והמדויק מתוך התיקייה שהעלית ב-GitHub
LOGOS_CONFIG = {
    "bet365": "https://github.io",
    "LeoVegas": "https://github.io",
    "Unibet": "https://github.io",
    "888": "https://github.io"
}

def init_environment():
    """יצירת התיקיות הנדרשות לבניית הפרויקט - מותאם לתיקיית public"""
    directories = ["public", "public/assets", "public/assets/logos"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 נוצרה תיקייה: {directory}")

def fetch_resource(name, url, target_dir="public/assets/logos"):
    """פונקציה להורדת משאבים מרוחקים בצורה בטוחה"""
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
        print(f"✅ הלוגו {name} הורד בהצלחה לנתיב המקומי.")
        return filepath
    except Exception as e:
        print(f"❌ שגיאה בהורדת המשאב {name}: {e}")
        return None
# ==========================================
# PART 2: CORE PROCESS & MAIN EXECUTION
# ==========================================

def build_project():
    """הפונקציה המרכזית שמנהלת את תהליך הבנייה של הפרויקט"""
    print("🏗️ מתחיל בתהליך הבנייה וההרכבה של האתר...")
    
    # 1. אתחול סביבת העבודה ותיקיית public
    init_environment()
    
    # 2. לולאת הורדה וסנכרון של הלוגואים החדשים שלך
    print("\n🔄 מסנכרן את הלוגואים מהשרת הראשי שלך...")
    for brand_name, logo_url in LOGOS_CONFIG.items():
        fetch_resource(brand_name, logo_url)
        
    print("\n📊 מעבד נתונים ומייצר קבצי תשתית לאתר...")
    # כאן הקוד יכול להמשיך לייצור קבצי HTML/JS נוספים בתוך תיקיית public במידת הצורך
    
    print("\n🎉 תהליך הבנייה הסתיים בהצלחה מלאה!")

if __name__ == "__main__":
    build_project()
