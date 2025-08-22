import json
import os
from datetime import datetime

def display_app_data(filename, category_name):
    """
    Display app data from a JSON file in a readable format
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n{'='*80}")
        print(f"{category_name.upper()} APPS DATA")
        print(f"{'='*80}")
        
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            total_count = result.get('total_count', 'Unknown')
            entries = result.get('entries', [])
            
            print(f"Total available apps: {total_count}")
            print(f"Fetched apps: {len(entries)}")
            print(f"Timestamp: {result.get('timestamp', 'Unknown')}")
            print(f"Category: {result.get('category', {}).get('name', 'Unknown')}")
            print(f"Subtype: {result.get('category', {}).get('subtype', 'Unknown')}")
            
            print(f"\n{'='*80}")
            print("TOP 20 APPS:")
            print(f"{'='*80}")
            
            for i, app in enumerate(entries[:20], 1):
                print(f"{i:2d}. {app.get('name', 'Unknown')}")
                print(f"    Developer: {app.get('developer', 'Unknown')}")
                print(f"    Price: {app.get('price', {}).get('price', 'Unknown')} {app.get('price', {}).get('currency', '')}")
                print(f"    Package: {app.get('vendor_identifier', 'Unknown')}")
                print()
        else:
            print("No data found in the file")
            
    except Exception as e:
        print(f"Error reading file {filename}: {str(e)}")

def main():
    """
    Display data from both free and grossing categories
    """
    data_dir = "appfigures_data"
    
    if not os.path.exists(data_dir):
        print("No data directory found. Please run fetch_appfigures_data.py first.")
        return
    
    # Find the most recent files for each category
    files = os.listdir(data_dir)
    free_files = [f for f in files if f.startswith('free_apps_')]
    grossing_files = [f for f in files if f.startswith('grossing_apps_')]
    
    if free_files:
        latest_free = max(free_files)
        display_app_data(os.path.join(data_dir, latest_free), "FREE")
    
    if grossing_files:
        latest_grossing = max(grossing_files)
        display_app_data(os.path.join(data_dir, latest_grossing), "GROSSING")
    
    if not free_files and not grossing_files:
        print("No data files found. Please run fetch_appfigures_data.py first.")

if __name__ == "__main__":
    main()
