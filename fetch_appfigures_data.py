import requests
import json
import time
from datetime import datetime
import os

class AppFiguresDataFetcher:
    def __init__(self):
        self.base_url = "https://appfigures.com/_u/api/ranks/snapshots"
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://appfigures.com/top-apps/google-play/malaysia/top-overall',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'x-rt': 'lXsfYyBP-MxeYZYKlm1mIZggEE1VzXE7Rrfo'
        }
        self.cookies = {
            'KSERVERID': '1755870775.347.100.338046|69c6428cdf95fffd388eca01de8b64ef',
            '_afm_session': 'ep1eqAYXD2HcZ0MN7Lc6MQ.mphC_In9ul9RTRqwjFYpjmiQzcy6kZ9WizHQVCSUr9z7fDDIp7jBIjw0QaKg8Cy5RE81TtvnSZsJAq3IRWBZjA.1755870774540.2592000000.EwW04cMCfZ02lIK7PN9hl3oxKCkcaIc8MGM6b1d1Rzo',
            'crisp-client%2Fsession%2F8be82478-7316-42dc-b8d4-fb27fbdf055d': 'session_8ea82548-292b-4e0e-a345-8a6bba609645',
            '_af_session': 'kbn4g32eyeeczrvsk3khgde0',
            '_af_session_verifier': '9fb37879-ada0-49c2-95ec-0cc452f30aaa'
        }
        
        # Create data directory if it doesn't exist
        self.data_dir = "appfigures_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def fetch_category_data(self, category_type, start=0, count=50):
        """
        Fetch data for a specific category (free or grossing)
        
        Args:
            category_type (str): Either 'free' or 'grossing'
            start (int): Starting position for pagination
            count (int): Number of results to fetch
        """
        # Try different approaches for free vs grossing
        if category_type == 'free':
            # For free apps, use the original parameters
            params = {
                'category': '100',  # Games category
                'country': 'MY',    # Malaysia
                'count': count,
                'start': start,
                'fields': 'results,id,entries,name,developer,developer_id,price,currency,storefront,vendor_identifier,category,subtype,timestamp,total_count'
            }
        elif category_type == 'grossing':
            # For grossing apps, try with different category or parameters
            params = {
                'category': '100',  # Games category
                'country': 'MY',    # Malaysia
                'count': count,
                'start': start,
                'fields': 'results,id,entries,name,developer,developer_id,price,currency,storefront,vendor_identifier,category,subtype,timestamp,total_count',
                'subtype': 'grossing'  # Try adding subtype for grossing
            }
        
        try:
            print(f"Fetching {category_type} apps data...")
            print(f"URL parameters: {params}")
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                cookies=self.cookies
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Successfully fetched {category_type} data")
                return data
            else:
                print(f"Error fetching {category_type} data: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception occurred while fetching {category_type} data: {str(e)}")
            return None

    def save_data(self, data, category_type):
        """
        Save the fetched data to a JSON file
        
        Args:
            data (dict): The data to save
            category_type (str): Category type for filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.data_dir}/{category_type}_apps_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return None

    def fetch_all_categories(self):
        """
        Fetch data for both free and grossing categories
        """
        categories = ['free', 'grossing']
        results = {}
        
        for category in categories:
            print(f"\n{'='*50}")
            print(f"Processing {category.upper()} category")
            print(f"{'='*50}")
            
            # Fetch data for the category
            data = self.fetch_category_data(category)
            
            if data:
                # Save the data
                saved_file = self.save_data(data, category)
                results[category] = {
                    'data': data,
                    'saved_file': saved_file
                }
                
                # Add a small delay between requests to be respectful
                time.sleep(1)
            else:
                print(f"Failed to fetch data for {category} category")
                results[category] = None
        
        return results

    def print_summary(self, results):
        """
        Print a summary of the fetched data
        
        Args:
            results (dict): Results from fetch_all_categories
        """
        print(f"\n{'='*60}")
        print("FETCH SUMMARY")
        print(f"{'='*60}")
        
        for category, result in results.items():
            if result and result['data']:
                # The data structure has results array with entries inside
                if 'results' in result['data'] and len(result['data']['results']) > 0:
                    first_result = result['data']['results'][0]
                    total_count = first_result.get('total_count', 'Unknown')
                    entries_count = len(first_result.get('entries', []))
                    print(f"{category.upper()} Category:")
                    print(f"  - Total available: {total_count}")
                    print(f"  - Fetched entries: {entries_count}")
                    print(f"  - Saved to: {result['saved_file']}")
                else:
                    print(f"{category.upper()} Category: No results found")
            else:
                print(f"{category.upper()} Category: FAILED")
            print()

def main():
    """
    Main function to execute the data fetching process
    """
    print("AppFigures Data Fetcher")
    print("Fetching data for FREE and GROSSING categories...")
    
    fetcher = AppFiguresDataFetcher()
    results = fetcher.fetch_all_categories()
    fetcher.print_summary(results)
    
    print("Data fetching completed!")

if __name__ == "__main__":
    main()
