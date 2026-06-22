"""
scripts/live_nav_fetch.py
Author: Manimaran_pro
Description: Fetches live and historical NAV details for specified mutual fund schemes 
             from the mfapi.in API and saves them to the data/raw/ directory.
"""

import os
import requests
import pandas as pd

# Global list of Mutual Fund AMFI Codes to fetch (Tasks 4 & 5)
SCHEME_CODES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

BASE_URL = "https://api.mfapi.in/mf/"

# Anchor output folder path to project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "raw")


def ensure_directory_exists(directory_path):
    """Checks if a directory exists, and if not, creates it."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")


def fetch_mutual_fund_data(scheme_code, scheme_name):
    """Connects to the API, downloads NAV details, and saves as CSV."""
    url = f"{BASE_URL}{scheme_code}"
    print(f"\nFetching data for {scheme_name} (Code: {scheme_code})...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data or "meta" not in data or "data" not in data:
            print(f"Warning: API returned incomplete data for code {scheme_code}.")
            return False
            
        meta_info = data["meta"]
        fund_house = meta_info.get("fund_house", "Unknown")
        scheme_type = meta_info.get("scheme_type", "Unknown")
        nav_list = data["data"]
        
        df = pd.DataFrame(nav_list)
        print(f"-> Fund House: {fund_house}")
        print(f"-> Records retrieved: {len(df)}")
        
        if "date" in df.columns and "nav" in df.columns:
            df["scheme_code"] = scheme_code
            df["scheme_name"] = scheme_name
            df = df[["scheme_code", "scheme_name", "date", "nav"]]
            
            output_file = os.path.join(OUTPUT_DIR, f"nav_history_{scheme_code}.csv")
            df.to_csv(output_file, index=False)
            print(f"-> Saved data to: {output_file}")
            return True
        else:
            print("Error: Columns 'date' or 'nav' were missing in the API response.")
            return False
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def main():
    ensure_directory_exists(OUTPUT_DIR)
    success_count = 0
    for code, name in SCHEME_CODES.items():
        success = fetch_mutual_fund_data(code, name)
        if success:
            success_count += 1
    print(f"\n--- API Fetch Complete: {success_count}/{len(SCHEME_CODES)} funds fetched. ---")


if __name__ == "__main__":
    main()