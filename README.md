# AppFigures Data Fetcher

This script fetches data from the AppFigures API for both "free" and "grossing" app categories in Japan's Google Play Store.

## Features

- Fetches data for both FREE and GROSSING app categories
- Saves data to JSON files with timestamps
- Handles pagination and error cases
- Provides detailed logging and summary

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script to fetch data for both categories:

```bash
python fetch_appfigures_data.py
```

## Output

The script will:
1. Create an `appfigures_data` directory
2. Fetch data for both free and grossing categories
3. Save the data to timestamped JSON files:
   - `free_apps_YYYYMMDD_HHMMSS.json`
   - `grossing_apps_YYYYMMDD_HHMMSS.json`

## Data Structure

The fetched data includes:
- App names and developers
- Pricing information
- Store identifiers
- Category and subtype information
- Timestamps

## Notes

- The script uses the exact headers and cookies from your provided curl command
- Data is fetched for Japan (JP) in the Games category (100)
- A 1-second delay is added between requests to be respectful to the API
- All data is saved with UTF-8 encoding to properly handle Japanese characters
