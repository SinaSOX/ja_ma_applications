import json
import os
from collections import Counter

def analyze_app_data(filename):
    """
    Analyze app data to understand the structure and identify free vs paid apps
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n{'='*80}")
        print(f"ANALYZING: {filename}")
        print(f"{'='*80}")
        
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            entries = result.get('entries', [])
            
            print(f"Total entries: {len(entries)}")
            print(f"Category: {result.get('category', {}).get('name', 'Unknown')}")
            print(f"Subtype: {result.get('category', {}).get('subtype', 'Unknown')}")
            
            # Analyze prices
            prices = []
            free_count = 0
            paid_count = 0
            
            for app in entries:
                price_info = app.get('price', {})
                price_str = price_info.get('price', '0.00')
                currency = price_info.get('currency', 'JPY')
                
                try:
                    price_float = float(price_str)
                    if price_float == 0.0:
                        free_count += 1
                    else:
                        paid_count += 1
                        prices.append(f"{price_str} {currency}")
                except ValueError:
                    prices.append(f"{price_str} {currency}")
            
            print(f"\nPrice Analysis:")
            print(f"  Free apps: {free_count}")
            print(f"  Paid apps: {paid_count}")
            
            if prices:
                print(f"  Paid app prices: {prices[:10]}")  # Show first 10 paid prices
            
            # Show some examples of apps
            print(f"\nSample Apps (first 10):")
            for i, app in enumerate(entries[:10], 1):
                price_str = app.get('price', {}).get('price', '0.00')
                currency = app.get('price', {}).get('currency', 'JPY')
                print(f"  {i:2d}. {app.get('name', 'Unknown')} - {price_str} {currency}")
            
            return {
                'total_entries': len(entries),
                'free_count': free_count,
                'paid_count': paid_count,
                'prices': prices,
                'subtype': result.get('category', {}).get('subtype', 'Unknown')
            }
        else:
            print("No data found")
            return None
            
    except Exception as e:
        print(f"Error analyzing {filename}: {str(e)}")
        return None

def main():
    """
    Analyze all data files
    """
    data_dir = "appfigures_data"
    
    if not os.path.exists(data_dir):
        print("No data directory found.")
        return
    
    files = os.listdir(data_dir)
    json_files = [f for f in files if f.endswith('.json')]
    
    if not json_files:
        print("No JSON files found.")
        return
    
    print("AppFigures Data Analysis")
    print("=" * 80)
    
    results = {}
    
    for filename in sorted(json_files):
        filepath = os.path.join(data_dir, filename)
        result = analyze_app_data(filepath)
        if result:
            results[filename] = result
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    
    for filename, result in results.items():
        print(f"\n{filename}:")
        print(f"  Subtype: {result['subtype']}")
        print(f"  Total apps: {result['total_entries']}")
        print(f"  Free apps: {result['free_count']}")
        print(f"  Paid apps: {result['paid_count']}")
        if result['paid_count'] > 0:
            print(f"  Paid prices: {result['prices'][:5]}")  # Show first 5

if __name__ == "__main__":
    main()
