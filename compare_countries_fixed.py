import json
import os
from collections import Counter, defaultdict
from datetime import datetime

class CountryComparisonFixed:
    def __init__(self):
        self.data_dir = "appfigures_data"
        self.countries = {
            'JP': 'Japan',
            'MY': 'Malaysia'
        }
        self.categories = ['free', 'grossing']
        
    def load_country_data(self):
        """
        Load data for both countries and categories
        """
        data = {}
        
        # Define the specific files for each country
        file_mapping = {
            'JP': {
                'free': 'free_apps_20250822_173324.json',
                'grossing': 'grossing_apps_20250822_173327.json'
            },
            'MY': {
                'free': 'free_apps_20250822_173642.json', 
                'grossing': 'grossing_apps_20250822_173644.json'
            }
        }
        
        for country_code, country_name in self.countries.items():
            data[country_code] = {}
            
            for category in self.categories:
                filename = file_mapping[country_code][category]
                filepath = os.path.join(self.data_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        country_data = json.load(f)
                        
                    # Extract apps from the data structure
                    if 'results' in country_data and len(country_data['results']) > 0:
                        apps = country_data['results'][0].get('entries', [])
                        data[country_code][category] = {
                            'apps': apps,
                            'total_count': country_data['results'][0].get('total_count', 0),
                            'timestamp': country_data['results'][0].get('timestamp', ''),
                            'currency': self.get_currency_from_apps(apps)
                        }
                    else:
                        data[country_code][category] = {'apps': [], 'total_count': 0}
                        
                except Exception as e:
                    print(f"Error loading {filepath}: {str(e)}")
                    data[country_code][category] = {'apps': [], 'total_count': 0}
        
        return data
    
    def get_currency_from_apps(self, apps):
        """
        Extract currency from the first app's price information
        """
        if apps and len(apps) > 0:
            return apps[0].get('price', {}).get('currency', 'Unknown')
        return 'Unknown'
    
    def compare_top_apps(self, data):
        """
        Compare top apps between countries
        """
        print("=" * 100)
        print("TOP APPS COMPARISON: JAPAN vs MALAYSIA")
        print("=" * 100)
        
        for category in self.categories:
            print(f"\n{'='*80}")
            print(f"{category.upper()} APPS COMPARISON")
            print(f"{'='*80}")
            
            jp_data = data['JP'].get(category, {})
            my_data = data['MY'].get(category, {})
            
            jp_apps = jp_data.get('apps', [])
            my_apps = my_data.get('apps', [])
            
            print(f"\nJapan ({len(jp_apps)} apps, {jp_data.get('currency', 'Unknown')}):")
            print("-" * 50)
            for i, app in enumerate(jp_apps[:10], 1):
                print(f"{i:2d}. {app.get('name', 'Unknown')} - {app.get('developer', 'Unknown')}")
            
            print(f"\nMalaysia ({len(my_apps)} apps, {my_data.get('currency', 'Unknown')}):")
            print("-" * 50)
            for i, app in enumerate(my_apps[:10], 1):
                print(f"{i:2d}. {app.get('name', 'Unknown')} - {app.get('developer', 'Unknown')}")
    
    def find_common_apps(self, data):
        """
        Find apps that appear in both countries
        """
        print(f"\n{'='*100}")
        print("COMMON APPS ANALYSIS")
        print(f"{'='*100}")
        
        for category in self.categories:
            print(f"\n{category.upper()} APPS - COMMON BETWEEN COUNTRIES:")
            print("-" * 60)
            
            jp_apps = data['JP'].get(category, {}).get('apps', [])
            my_apps = data['MY'].get(category, {}).get('apps', [])
            
            # Get app names and their positions
            jp_app_names = {app.get('name', ''): i+1 for i, app in enumerate(jp_apps)}
            my_app_names = {app.get('name', ''): i+1 for i, app in enumerate(my_apps)}
            
            # Find common apps
            common_apps = set(jp_app_names.keys()) & set(my_app_names.keys())
            
            if common_apps:
                print(f"Found {len(common_apps)} common apps:")
                for app_name in sorted(common_apps):
                    jp_pos = jp_app_names[app_name]
                    my_pos = my_app_names[app_name]
                    print(f"  {app_name}:")
                    print(f"    Japan: #{jp_pos}, Malaysia: #{my_pos}")
            else:
                print("No common apps found.")
    
    def analyze_developers(self, data):
        """
        Analyze top developers in each country
        """
        print(f"\n{'='*100}")
        print("TOP DEVELOPERS ANALYSIS")
        print(f"{'='*100}")
        
        for category in self.categories:
            print(f"\n{category.upper()} APPS - TOP DEVELOPERS:")
            print("-" * 60)
            
            for country_code, country_name in self.countries.items():
                apps = data[country_code].get(category, {}).get('apps', [])
                
                # Count developers
                developers = [app.get('developer', 'Unknown') for app in apps]
                developer_counts = Counter(developers)
                
                print(f"\n{country_name} Top Developers:")
                for developer, count in developer_counts.most_common(5):
                    print(f"  {developer}: {count} apps")
    
    def analyze_app_categories(self, data):
        """
        Analyze app types and categories
        """
        print(f"\n{'='*100}")
        print("APP CATEGORY ANALYSIS")
        print(f"{'='*100}")
        
        for category in self.categories:
            print(f"\n{category.upper()} APPS - CATEGORY ANALYSIS:")
            print("-" * 60)
            
            for country_code, country_name in self.countries.items():
                apps = data[country_code].get(category, {}).get('apps', [])
                
                # Analyze app names for patterns
                app_names = [app.get('name', '').lower() for app in apps]
                
                # Look for common keywords
                keywords = ['game', 'social', 'utility', 'entertainment', 'productivity', 'finance', 'health', 'pdf', 'reader', 'wallet', 'bank', 'payment']
                keyword_counts = defaultdict(int)
                
                for name in app_names:
                    for keyword in keywords:
                        if keyword in name:
                            keyword_counts[keyword] += 1
                
                print(f"\n{country_name} App Types:")
                for keyword, count in sorted(keyword_counts.items()):
                    if count > 0:
                        print(f"  {keyword.capitalize()}: {count} apps")
    
    def generate_summary_report(self, data):
        """
        Generate a comprehensive summary report
        """
        print(f"\n{'='*100}")
        print("COMPREHENSIVE SUMMARY REPORT")
        print(f"{'='*100}")
        
        print(f"\nData Collection Summary:")
        print("-" * 40)
        for country_code, country_name in self.countries.items():
            for category in self.categories:
                category_data = data[country_code].get(category, {})
                apps = category_data.get('apps', [])
                currency = category_data.get('currency', 'Unknown')
                timestamp = category_data.get('timestamp', 'Unknown')
                
                print(f"{country_name} {category.capitalize()}: {len(apps)} apps, {currency}, {timestamp}")
        
        print(f"\nKey Findings:")
        print("-" * 40)
        
        # Compare top apps
        for category in self.categories:
            jp_top = data['JP'].get(category, {}).get('apps', [])
            my_top = data['MY'].get(category, {}).get('apps', [])
            
            if jp_top and my_top:
                jp_top_app = jp_top[0].get('name', 'Unknown') if jp_top else 'None'
                my_top_app = my_top[0].get('name', 'Unknown') if my_top else 'None'
                
                print(f"Top {category} app in Japan: {jp_top_app}")
                print(f"Top {category} app in Malaysia: {my_top_app}")
                print()
        
        # Currency differences
        jp_currency = data['JP'].get('free', {}).get('currency', 'Unknown')
        my_currency = data['MY'].get('free', {}).get('currency', 'Unknown')
        print(f"Currency: Japan uses {jp_currency}, Malaysia uses {my_currency}")
        
        # Unique apps analysis
        print(f"\nUnique Apps Analysis:")
        print("-" * 40)
        for category in self.categories:
            jp_apps = set(app.get('name', '') for app in data['JP'].get(category, {}).get('apps', []))
            my_apps = set(app.get('name', '') for app in data['MY'].get(category, {}).get('apps', []))
            
            jp_only = jp_apps - my_apps
            my_only = my_apps - jp_apps
            
            print(f"{category.capitalize()} apps:")
            print(f"  Japan only: {len(jp_only)} apps")
            print(f"  Malaysia only: {len(my_only)} apps")
            print(f"  Common: {len(jp_apps & my_apps)} apps")

def main():
    """
    Main function to run the comparison
    """
    print("AppFigures Country Comparison Tool (Fixed)")
    print("Comparing Japan vs Malaysia App Data")
    print("=" * 100)
    
    comparator = CountryComparisonFixed()
    
    # Load data
    print("Loading data...")
    data = comparator.load_country_data()
    
    # Run comparisons
    comparator.compare_top_apps(data)
    comparator.find_common_apps(data)
    comparator.analyze_developers(data)
    comparator.analyze_app_categories(data)
    comparator.generate_summary_report(data)
    
    print(f"\n{'='*100}")
    print("COMPARISON COMPLETED")
    print(f"{'='*100}")

if __name__ == "__main__":
    main()
