import requests
import json
import time
from datetime import datetime
import os

class AppFiguresAdvancedFetcher:
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

    def fetch_with_params(self, params, description):
        """
        Fetch data with specific parameters
        """
        try:
            print(f"\nTrying: {description}")
            print(f"Parameters: {params}")
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                cookies=self.cookies
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    result = data['results'][0]
                    subtype = result.get('category', {}).get('subtype', 'unknown')
                    total_count = result.get('total_count', 0)
                    entries_count = len(result.get('entries', []))
                    print(f"✓ Success! Subtype: {subtype}, Total: {total_count}, Entries: {entries_count}")
                    return data
                else:
                    print("✗ No results found")
                    return None
            else:
                print(f"✗ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return None

    def try_different_approaches(self):
        """
        Try different parameter combinations to get free vs grossing data
        """
        base_params = {
            'country': 'MY',
            'count': '50',
            'start': '0',
            'fields': 'results,id,entries,name,developer,developer_id,price,currency,storefront,vendor_identifier,category,subtype,timestamp,total_count'
        }
        
        approaches = [
            # Approach 1: Original parameters (should give free)
            {
                'params': {**base_params, 'category': '100'},
                'description': 'Original parameters (category=100)'
            },
            # Approach 2: Try with subtype=free
            {
                'params': {**base_params, 'category': '100', 'subtype': 'free'},
                'description': 'With subtype=free'
            },
            # Approach 3: Try with subtype=grossing
            {
                'params': {**base_params, 'category': '100', 'subtype': 'grossing'},
                'description': 'With subtype=grossing'
            },
            # Approach 4: Try different category ID for grossing
            {
                'params': {**base_params, 'category': '101'},
                'description': 'Different category ID (101)'
            },
            # Approach 5: Try without category
            {
                'params': {**base_params},
                'description': 'Without category parameter'
            },
            # Approach 6: Try with different start position
            {
                'params': {**base_params, 'category': '100', 'start': '150'},
                'description': 'With start=150 (original curl)'
            }
        ]
        
        results = {}
        
        for i, approach in enumerate(approaches, 1):
            print(f"\n{'='*60}")
            print(f"APPROACH {i}")
            print(f"{'='*60}")
            
            data = self.fetch_with_params(approach['params'], approach['description'])
            if data:
                results[f"approach_{i}"] = {
                    'data': data,
                    'description': approach['description'],
                    'params': approach['params']
                }
            
            # Add delay between requests
            time.sleep(2)
        
        return results

    def save_results(self, results):
        """
        Save all results to files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for approach_name, result in results.items():
            if result['data']:
                # Extract subtype from the data
                if 'results' in result['data'] and len(result['data']['results']) > 0:
                    subtype = result['data']['results'][0].get('category', {}).get('subtype', 'unknown')
                    filename = f"{self.data_dir}/{approach_name}_{subtype}_{timestamp}.json"
                else:
                    filename = f"{self.data_dir}/{approach_name}_{timestamp}.json"
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(result['data'], f, indent=2, ensure_ascii=False)
                    print(f"Saved: {filename}")
                except Exception as e:
                    print(f"Error saving {filename}: {str(e)}")

def main():
    """
    Main function to try different approaches
    """
    print("AppFigures Advanced Data Fetcher")
    print("Trying different parameter combinations...")
    
    fetcher = AppFiguresAdvancedFetcher()
    results = fetcher.try_different_approaches()
    fetcher.save_results(results)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Successful approaches: {len(results)}")
    for approach_name, result in results.items():
        print(f"- {approach_name}: {result['description']}")

if __name__ == "__main__":
    main()
