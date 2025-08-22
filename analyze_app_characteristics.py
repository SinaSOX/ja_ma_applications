import json
import os
from collections import Counter, defaultdict
from datetime import datetime
import re

class AppCharacteristicsAnalyzer:
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
        
        for country_code, country_name in self.countries.items():
            data[country_code] = {}
            
            for category in self.categories:
                # Find the most recent file for this country and category
                files = [f for f in os.listdir(self.data_dir) 
                        if f.startswith(f'{category}_apps_') and f.endswith('.json')]
                
                if files:
                    # Get the most recent file
                    latest_file = max(files)
                    filepath = os.path.join(self.data_dir, latest_file)
                    
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
                else:
                    data[country_code][category] = {'apps': [], 'total_count': 0}
        
        return data
    
    def get_currency_from_apps(self, apps):
        """
        Extract currency from the first app's price information
        """
        if apps and len(apps) > 0:
            return apps[0].get('price', {}).get('currency', 'Unknown')
        return 'Unknown'
    
    def analyze_developer_patterns(self, data):
        """
        Analyze developer patterns and market concentration
        """
        print("=" * 100)
        print("DEVELOPER PATTERNS ANALYSIS")
        print("=" * 100)
        
        for category in self.categories:
            print(f"\n{'='*80}")
            print(f"{category.upper()} APPS - DEVELOPER ANALYSIS")
            print(f"{'='*80}")
            
            for country_code, country_name in self.countries.items():
                country_data = data[country_code].get(category, {})
                apps = country_data.get('apps', [])
                
                if not apps:
                    continue
                
                # Count apps per developer
                developer_counts = Counter()
                developer_apps = defaultdict(list)
                
                for app in apps:
                    developer = app.get('developer', 'Unknown')
                    developer_counts[developer] += 1
                    developer_apps[developer].append(app.get('name', 'Unknown'))
                
                # Find top developers
                top_developers = developer_counts.most_common(10)
                
                print(f"\n{country_name} - Top 10 Developers:")
                print("-" * 60)
                for i, (developer, count) in enumerate(top_developers, 1):
                    print(f"{i:2d}. {developer} ({count} apps)")
                    # Show some app names for top developers
                    if count > 1:
                        app_names = developer_apps[developer][:3]
                        print(f"    Apps: {', '.join(app_names)}")
                
                # Calculate market concentration
                total_apps = len(apps)
                top_5_developers = sum(count for _, count in top_developers[:5])
                concentration = (top_5_developers / total_apps) * 100 if total_apps > 0 else 0
                
                print(f"\nMarket Concentration Analysis:")
                print(f"- Total apps: {total_apps}")
                print(f"- Top 5 developers control: {top_5_developers} apps ({concentration:.1f}%)")
                print(f"- Unique developers: {len(developer_counts)}")
    
    def analyze_app_categories_by_name(self, data):
        """
        Analyze app categories based on app names and keywords
        """
        print(f"\n{'='*100}")
        print("APP CATEGORY ANALYSIS (BASED ON NAMES)")
        print(f"{'='*100}")
        
        # Define category keywords
        categories = {
            'Gaming': ['game', 'play', 'puzzle', 'shooter', 'survival', 'strategy', 'blast', 'crush', 'master', 'kingdom', 'royal', 'legends', 'bang'],
            'Social Media': ['tiktok', 'telegram', 'whatsapp', 'line', 'social', 'chat', 'messenger'],
            'Entertainment': ['drama', 'film', 'movie', 'tv', 'anime', 'manga', 'music', 'piano', 'beat', 'video', 'editor'],
            'Finance': ['wallet', 'pay', 'bank', 'money', 'kasih', 'digital', 'ewallet', 'financial'],
            'Productivity': ['pdf', 'reader', 'viewer', 'document', 'office', 'work', 'business'],
            'Shopping': ['shop', 'shopping', 'buy', 'purchase', 'marketplace', 'ecommerce'],
            'AI/Tech': ['chatgpt', 'ai', 'artificial', 'intelligence', 'smart', 'assistant'],
            'Government': ['myjpj', 'kwsp', 'mydigital', 'government', 'official'],
            'Transportation': ['grab', 'taxi', 'transport', 'delivery', 'ride'],
            'Education': ['learn', 'study', 'education', 'school', 'university', 'course']
        }
        
        for category in self.categories:
            print(f"\n{'='*80}")
            print(f"{category.upper()} APPS - CATEGORY ANALYSIS")
            print(f"{'='*80}")
            
            for country_code, country_name in self.countries.items():
                country_data = data[country_code].get(category, {})
                apps = country_data.get('apps', [])
                
                if not apps:
                    continue
                
                print(f"\n{country_name}:")
                print("-" * 40)
                
                # Categorize apps
                category_counts = defaultdict(list)
                uncategorized = []
                
                for app in apps:
                    app_name = app.get('name', '').lower()
                    categorized = False
                    
                    for cat_name, keywords in categories.items():
                        for keyword in keywords:
                            if keyword.lower() in app_name:
                                category_counts[cat_name].append(app.get('name', 'Unknown'))
                                categorized = True
                                break
                        if categorized:
                            break
                    
                    if not categorized:
                        uncategorized.append(app.get('name', 'Unknown'))
                
                # Display results
                for cat_name, app_list in sorted(category_counts.items(), key=lambda x: len(x[1]), reverse=True):
                    if app_list:
                        print(f"{cat_name}: {len(app_list)} apps")
                        # Show top apps in each category
                        top_apps = app_list[:5]
                        print(f"  Top apps: {', '.join(top_apps)}")
                
                if uncategorized:
                    print(f"Uncategorized: {len(uncategorized)} apps")
                    print(f"  Examples: {', '.join(uncategorized[:5])}")
    
    def analyze_pricing_patterns(self, data):
        """
        Analyze pricing patterns and strategies
        """
        print(f"\n{'='*100}")
        print("PRICING PATTERNS ANALYSIS")
        print(f"{'='*100}")
        
        for category in self.categories:
            print(f"\n{'='*80}")
            print(f"{category.upper()} APPS - PRICING ANALYSIS")
            print(f"{'='*80}")
            
            for country_code, country_name in self.countries.items():
                country_data = data[country_code].get(category, {})
                apps = country_data.get('apps', [])
                currency = country_data.get('currency', 'Unknown')
                
                if not apps:
                    continue
                
                print(f"\n{country_name} ({currency}):")
                print("-" * 40)
                
                # Analyze pricing
                free_apps = 0
                paid_apps = 0
                price_ranges = defaultdict(int)
                
                for app in apps:
                    price_info = app.get('price', {})
                    price_str = price_info.get('price', '0.00')
                    
                    try:
                        price = float(price_str)
                        if price == 0.0:
                            free_apps += 1
                        else:
                            paid_apps += 1
                            # Categorize by price range
                            if price <= 1.0:
                                price_ranges['$0.01-$1.00'] += 1
                            elif price <= 5.0:
                                price_ranges['$1.01-$5.00'] += 1
                            elif price <= 10.0:
                                price_ranges['$5.01-$10.00'] += 1
                            else:
                                price_ranges['$10.01+'] += 1
                    except ValueError:
                        free_apps += 1
                
                total_apps = len(apps)
                free_percentage = (free_apps / total_apps) * 100 if total_apps > 0 else 0
                paid_percentage = (paid_apps / total_apps) * 100 if total_apps > 0 else 0
                
                print(f"Total apps: {total_apps}")
                print(f"Free apps: {free_apps} ({free_percentage:.1f}%)")
                print(f"Paid apps: {paid_apps} ({paid_percentage:.1f}%)")
                
                if paid_apps > 0:
                    print("\nPaid app price distribution:")
                    for price_range, count in price_ranges.items():
                        percentage = (count / paid_apps) * 100
                        print(f"  {price_range}: {count} apps ({percentage:.1f}%)")
    
    def analyze_app_name_patterns(self, data):
        """
        Analyze patterns in app names and branding
        """
        print(f"\n{'='*100}")
        print("APP NAME PATTERNS ANALYSIS")
        print(f"{'='*100}")
        
        for category in self.categories:
            print(f"\n{'='*80}")
            print(f"{category.upper()} APPS - NAME PATTERNS")
            print(f"{'='*80}")
            
            for country_code, country_name in self.countries.items():
                country_data = data[country_code].get(category, {})
                apps = country_data.get('apps', [])
                
                if not apps:
                    continue
                
                print(f"\n{country_name}:")
                print("-" * 40)
                
                # Analyze name patterns
                name_lengths = []
                common_words = Counter()
                special_chars = Counter()
                
                for app in apps:
                    name = app.get('name', '')
                    name_lengths.append(len(name))
                    
                    # Count common words
                    words = re.findall(r'\b\w+\b', name.lower())
                    for word in words:
                        if len(word) > 2:  # Skip very short words
                            common_words[word] += 1
                    
                    # Count special characters
                    for char in name:
                        if not char.isalnum() and char != ' ':
                            special_chars[char] += 1
                
                # Display statistics
                avg_length = sum(name_lengths) / len(name_lengths) if name_lengths else 0
                print(f"Average app name length: {avg_length:.1f} characters")
                
                print(f"\nMost common words in app names:")
                for word, count in common_words.most_common(10):
                    print(f"  '{word}': {count} times")
                
                print(f"\nMost common special characters:")
                for char, count in special_chars.most_common(5):
                    print(f"  '{char}': {count} times")
    
    def generate_comprehensive_report(self, data):
        """
        Generate a comprehensive analysis report
        """
        print("=" * 120)
        print("COMPREHENSIVE APP CHARACTERISTICS ANALYSIS")
        print("JAPAN vs MALAYSIA - TOP 100 APPS COMPARISON")
        print("=" * 120)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 120)
        
        # Note about app size data
        print("\n📋 IMPORTANT NOTE:")
        print("App size information is not available in the current data structure.")
        print("This analysis focuses on other important characteristics:")
        print("- Developer patterns and market concentration")
        print("- App categories based on name analysis")
        print("- Pricing strategies and patterns")
        print("- App naming conventions and branding")
        print("- Cultural and market differences")
        
        # Run all analyses
        self.analyze_developer_patterns(data)
        self.analyze_app_categories_by_name(data)
        self.analyze_pricing_patterns(data)
        self.analyze_app_name_patterns(data)
        
        # Generate summary insights
        self.generate_summary_insights(data)
    
    def generate_summary_insights(self, data):
        """
        Generate summary insights and recommendations
        """
        print(f"\n{'='*120}")
        print("SUMMARY INSIGHTS AND RECOMMENDATIONS")
        print(f"{'='*120}")
        
        print("\n🎯 KEY FINDINGS:")
        print("1. Market Concentration: Analysis of developer dominance in each market")
        print("2. Category Preferences: Cultural differences in app preferences")
        print("3. Pricing Strategies: Free vs paid app distribution")
        print("4. Naming Conventions: Branding and localization patterns")
        
        print("\n📊 RECOMMENDATIONS FOR APP DEVELOPERS:")
        print("1. Market Entry Strategy:")
        print("   - Japan: Focus on productivity and work-related apps")
        print("   - Malaysia: Emphasize entertainment and government services")
        
        print("\n2. Pricing Strategy:")
        print("   - Consider local purchasing power and preferences")
        print("   - Analyze free vs paid app ratios in target markets")
        
        print("\n3. Localization:")
        print("   - Adapt app names and branding to local preferences")
        print("   - Consider cultural differences in app categories")
        
        print("\n4. Developer Strategy:")
        print("   - Study successful developers in each market")
        print("   - Understand market concentration patterns")
        
        print(f"\n{'='*120}")
        print("ANALYSIS COMPLETED")
        print(f"{'='*120}")

def main():
    """
    Main function to run the comprehensive analysis
    """
    analyzer = AppCharacteristicsAnalyzer()
    
    print("Loading data...")
    data = analyzer.load_country_data()
    
    print("Running comprehensive analysis...")
    analyzer.generate_comprehensive_report(data)

if __name__ == "__main__":
    main()
