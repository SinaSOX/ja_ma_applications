import json
import os
from collections import Counter

class Top100Comparison:
    def __init__(self):
        self.data_dir = "appfigures_data"
        
        # Define the specific files for each country
        self.file_mapping = {
            'JP': {
                'free': 'free_apps_20250822_173324.json',
                'grossing': 'grossing_apps_20250822_173327.json'
            },
            'MY': {
                'free': 'free_apps_20250822_173642.json', 
                'grossing': 'grossing_apps_20250822_173644.json'
            }
        }
    
    def load_data(self):
        """
        Load data for both countries
        """
        data = {}
        
        for country_code in ['JP', 'MY']:
            data[country_code] = {}
            
            for category in ['free', 'grossing']:
                filename = self.file_mapping[country_code][category]
                filepath = os.path.join(self.data_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        country_data = json.load(f)
                        
                    if 'results' in country_data and len(country_data['results']) > 0:
                        apps = country_data['results'][0].get('entries', [])
                        data[country_code][category] = apps
                    else:
                        data[country_code][category] = []
                        
                except Exception as e:
                    print(f"Error loading {filepath}: {str(e)}")
                    data[country_code][category] = []
        
        return data
    
    def compare_top100_apps(self, data):
        """
        Compare top 100 apps between countries
        """
        print("=" * 120)
        print("مقایسه ۱۰۰ اپلیکیشن برتر ژاپن و مالزی")
        print("=" * 120)
        
        for category in ['free', 'grossing']:
            print(f"\n{'='*100}")
            print(f"اپلیکیشن‌های {category.upper()} - ۱۰۰ اپلیکیشن برتر")
            print(f"{'='*100}")
            
            jp_apps = data['JP'].get(category, [])
            my_apps = data['MY'].get(category, [])
            
            print(f"\n{'='*50} ژاپن {'='*50}")
            print(f"{'رتبه':<4} {'نام اپلیکیشن':<40} {'توسعه‌دهنده':<30} {'ارز':<6}")
            print("-" * 100)
            
            for i, app in enumerate(jp_apps[:100], 1):
                name = app.get('name', 'Unknown')
                developer = app.get('developer', 'Unknown')
                currency = app.get('price', {}).get('currency', 'Unknown')
                print(f"{i:<4} {name:<40} {developer:<30} {currency:<6}")
            
            print(f"\n{'='*50} مالزی {'='*50}")
            print(f"{'رتبه':<4} {'نام اپلیکیشن':<40} {'توسعه‌دهنده':<30} {'ارز':<6}")
            print("-" * 100)
            
            for i, app in enumerate(my_apps[:100], 1):
                name = app.get('name', 'Unknown')
                developer = app.get('developer', 'Unknown')
                currency = app.get('price', {}).get('currency', 'Unknown')
                print(f"{i:<4} {name:<40} {developer:<30} {currency:<6}")
    
    def find_common_apps_in_top100(self, data):
        """
        Find common apps in top 100 between countries
        """
        print(f"\n{'='*120}")
        print("اپلیکیشن‌های مشترک در ۱۰۰ اپلیکیشن برتر")
        print(f"{'='*120}")
        
        for category in ['free', 'grossing']:
            print(f"\n{category.upper()} APPS:")
            print("-" * 60)
            
            jp_apps = data['JP'].get(category, [])
            my_apps = data['MY'].get(category, [])
            
            # Get top 100 app names and their positions
            jp_top100_names = {app.get('name', ''): i+1 for i, app in enumerate(jp_apps[:100])}
            my_top100_names = {app.get('name', ''): i+1 for i, app in enumerate(my_apps[:100])}
            
            # Find common apps in top 100
            common_apps = set(jp_top100_names.keys()) & set(my_top100_names.keys())
            
            if common_apps:
                print(f"تعداد اپلیکیشن‌های مشترک در ۱۰۰ اپلیکیشن برتر: {len(common_apps)}")
                print(f"{'نام اپلیکیشن':<40} {'رتبه در ژاپن':<15} {'رتبه در مالزی':<15}")
                print("-" * 70)
                
                for app_name in sorted(common_apps):
                    jp_pos = jp_top100_names[app_name]
                    my_pos = my_top100_names[app_name]
                    print(f"{app_name:<40} #{jp_pos:<14} #{my_pos:<14}")
            else:
                print("هیچ اپلیکیشن مشترکی در ۱۰۰ اپلیکیشن برتر یافت نشد.")
    
    def analyze_developer_dominance(self, data):
        """
        Analyze which developers dominate the top 100
        """
        print(f"\n{'='*120}")
        print("تحلیل تسلط توسعه‌دهندگان در ۱۰۰ اپلیکیشن برتر")
        print(f"{'='*120}")
        
        for category in ['free', 'grossing']:
            print(f"\n{category.upper()} APPS:")
            print("-" * 60)
            
            for country_code, country_name in [('JP', 'ژاپن'), ('MY', 'مالزی')]:
                apps = data[country_code].get(category, [])
                top100_apps = apps[:100]
                
                # Count developers in top 100
                developers = [app.get('developer', 'Unknown') for app in top100_apps]
                developer_counts = Counter(developers)
                
                print(f"\n{country_name} - توسعه‌دهندگان برتر در ۱۰۰ اپلیکیشن اول:")
                print(f"{'توسعه‌دهنده':<40} {'تعداد اپلیکیشن':<15}")
                print("-" * 55)
                
                for developer, count in developer_counts.most_common(10):
                    print(f"{developer:<40} {count:<15}")
    
    def compare_app_categories_top100(self, data):
        """
        Compare app categories in top 100
        """
        print(f"\n{'='*120}")
        print("تحلیل دسته‌بندی اپلیکیشن‌ها در ۱۰۰ اپلیکیشن برتر")
        print(f"{'='*120}")
        
        for category in ['free', 'grossing']:
            print(f"\n{category.upper()} APPS:")
            print("-" * 60)
            
            for country_code, country_name in [('JP', 'ژاپن'), ('MY', 'مالزی')]:
                apps = data[country_code].get(category, [])
                top100_apps = apps[:100]
                
                # Analyze app names for patterns
                app_names = [app.get('name', '').lower() for app in top100_apps]
                
                # Look for common keywords
                keywords = ['game', 'social', 'utility', 'entertainment', 'productivity', 
                           'finance', 'health', 'pdf', 'reader', 'wallet', 'bank', 
                           'payment', 'ai', 'chat', 'video', 'music', 'photo', 'drama',
                           'shopping', 'food', 'travel', 'education', 'fitness', 'weather']
                
                keyword_counts = {}
                for keyword in keywords:
                    count = sum(1 for name in app_names if keyword in name)
                    if count > 0:
                        keyword_counts[keyword] = count
                
                print(f"\n{country_name} - دسته‌بندی اپلیکیشن‌ها:")
                print(f"{'دسته‌بندی':<20} {'تعداد':<10}")
                print("-" * 30)
                
                for keyword, count in sorted(keyword_counts.items()):
                    print(f"{keyword.capitalize():<20} {count:<10}")
    
    def generate_detailed_summary(self, data):
        """
        Generate detailed summary of top 100 comparison
        """
        print(f"\n{'='*120}")
        print("خلاصه تفصیلی مقایسه ۱۰۰ اپلیکیشن برتر")
        print(f"{'='*120}")
        
        for category in ['free', 'grossing']:
            print(f"\n{category.upper()} APPS - خلاصه:")
            print("-" * 50)
            
            jp_apps = data['JP'].get(category, [])
            my_apps = data['MY'].get(category, [])
            
            jp_top100 = jp_apps[:100]
            my_top100 = my_apps[:100]
            
            # Common apps in top 100
            jp_names = {app.get('name', '') for app in jp_top100}
            my_names = {app.get('name', '') for app in my_top100}
            common_in_top100 = jp_names & my_names
            
            print(f"تعداد اپلیکیشن‌های مشترک در ۱۰۰ اپلیکیشن برتر: {len(common_in_top100)}")
            print(f"تعداد اپلیکیشن‌های منحصر به ژاپن: {len(jp_names - my_names)}")
            print(f"تعداد اپلیکیشن‌های منحصر به مالزی: {len(my_names - jp_names)}")
            
            # Top developers in top 100
            jp_developers = [app.get('developer', 'Unknown') for app in jp_top100]
            my_developers = [app.get('developer', 'Unknown') for app in my_top100]
            
            jp_top_dev = Counter(jp_developers).most_common(1)[0] if jp_developers else ('None', 0)
            my_top_dev = Counter(my_developers).most_common(1)[0] if my_developers else ('None', 0)
            
            print(f"توسعه‌دهنده برتر در ژاپن: {jp_top_dev[0]} ({jp_top_dev[1]} اپلیکیشن)")
            print(f"توسعه‌دهنده برتر در مالزی: {my_top_dev[0]} ({my_top_dev[1]} اپلیکیشن)")

def main():
    """
    Main function to run the top 20 comparison
    """
    print("مقایسه ۱۰۰ اپلیکیشن برتر ژاپن و مالزی")
    print("=" * 120)
    
    comparator = Top100Comparison()
    
    # Load data
    print("در حال بارگذاری داده‌ها...")
    data = comparator.load_data()
    
    # Run comparisons
    comparator.compare_top100_apps(data)
    comparator.find_common_apps_in_top100(data)
    comparator.analyze_developer_dominance(data)
    comparator.compare_app_categories_top100(data)
    comparator.generate_detailed_summary(data)
    
    print(f"\n{'='*120}")
    print("مقایسه ۱۰۰ اپلیکیشن برتر تکمیل شد")
    print(f"{'='*120}")

if __name__ == "__main__":
    main()
