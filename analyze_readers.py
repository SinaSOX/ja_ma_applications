import json
import os
from collections import Counter

def analyze_reader_apps():
    """
    Analyze what types of reader apps are popular in Japan
    """
    print("تحلیل اپلیکیشن‌های Reader در ژاپن")
    print("=" * 60)
    
    # Load Japanese data
    jp_file = "appfigures_data/free_apps_20250822_173324.json"
    
    try:
        with open(jp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'results' in data and len(data['results']) > 0:
            apps = data['results'][0].get('entries', [])
            
            # Find all apps with "reader" in the name (case insensitive)
            reader_apps = []
            for app in apps:
                name = app.get('name', '').lower()
                if 'reader' in name or 'pdf' in name:
                    reader_apps.append({
                        'name': app.get('name', ''),
                        'developer': app.get('developer', ''),
                        'position': apps.index(app) + 1
                    })
            
            print(f"تعداد اپلیکیشن‌های Reader یافت شده: {len(reader_apps)}")
            print("\nاپلیکیشن‌های Reader در ژاپن:")
            print("-" * 80)
            
            for app in reader_apps:
                print(f"رتبه {app['position']:2d}: {app['name']}")
                print(f"         توسعه‌دهنده: {app['developer']}")
                print()
            
            # Categorize reader types
            categories = {
                'PDF Reader': [],
                'Document Reader': [],
                'Other Reader': []
            }
            
            for app in reader_apps:
                name = app['name'].lower()
                if 'pdf' in name:
                    categories['PDF Reader'].append(app)
                elif 'document' in name:
                    categories['Document Reader'].append(app)
                else:
                    categories['Other Reader'].append(app)
            
            print("دسته‌بندی اپلیکیشن‌های Reader:")
            print("-" * 40)
            
            for category, apps_list in categories.items():
                if apps_list:
                    print(f"\n{category} ({len(apps_list)} اپلیکیشن):")
                    for app in apps_list:
                        print(f"  - {app['name']} (رتبه {app['position']})")
            
            # Check for other reading-related apps
            print(f"\n{'='*60}")
            print("جستجوی اپلیکیشن‌های مرتبط با خواندن:")
            print("-" * 60)
            
            reading_keywords = ['book', 'manga', 'comic', 'novel', 'text', 'document', 'viewer']
            reading_apps = []
            
            for app in apps:
                name = app.get('name', '').lower()
                for keyword in reading_keywords:
                    if keyword in name:
                        reading_apps.append({
                            'name': app.get('name', ''),
                            'developer': app.get('developer', ''),
                            'position': apps.index(app) + 1,
                            'keyword': keyword
                        })
                        break
            
            if reading_apps:
                print(f"تعداد اپلیکیشن‌های مرتبط با خواندن: {len(reading_apps)}")
                for app in reading_apps:
                    print(f"رتبه {app['position']:2d}: {app['name']} (کلیدواژه: {app['keyword']})")
                    print(f"         توسعه‌دهنده: {app['developer']}")
                    print()
            else:
                print("هیچ اپلیکیشن مرتبط با خواندن یافت نشد.")
                
    except Exception as e:
        print(f"خطا در خواندن فایل: {str(e)}")

def compare_with_malaysia():
    """
    Compare reader apps between Japan and Malaysia
    """
    print(f"\n{'='*60}")
    print("مقایسه اپلیکیشن‌های Reader بین ژاپن و مالزی")
    print("=" * 60)
    
    countries = {
        'JP': 'appfigures_data/free_apps_20250822_173324.json',
        'MY': 'appfigures_data/free_apps_20250822_173642.json'
    }
    
    for country_code, filepath in countries.items():
        country_name = 'ژاپن' if country_code == 'JP' else 'مالزی'
        print(f"\n{country_name}:")
        print("-" * 30)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'results' in data and len(data['results']) > 0:
                apps = data['results'][0].get('entries', [])
                
                # Find reader apps
                reader_apps = []
                for app in apps:
                    name = app.get('name', '').lower()
                    if 'reader' in name or 'pdf' in name:
                        reader_apps.append({
                            'name': app.get('name', ''),
                            'position': apps.index(app) + 1
                        })
                
                print(f"تعداد اپلیکیشن‌های Reader: {len(reader_apps)}")
                for app in reader_apps:
                    print(f"  رتبه {app['position']:2d}: {app['name']}")
                    
        except Exception as e:
            print(f"خطا در خواندن فایل {country_name}: {str(e)}")

if __name__ == "__main__":
    analyze_reader_apps()
    compare_with_malaysia()
