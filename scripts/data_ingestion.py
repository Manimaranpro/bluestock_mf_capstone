"""
scripts/data_ingestion.py
Author: Manimaran_pro
Description: Validates, profiles, and analyzes the 10 core mutual fund datasets
             provided for the Bluestock Mutual Fund Analytics platform.
"""

import os
import pandas as pd

# Anchor path logic to find data/raw folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DATA_DIR = os.path.join(ROOT_DIR, "data", "raw")

# Names of the 10 CSV datasets (must be inside data/raw/)
EXPECTED_FILES = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip.csv",
    "05_category_inflows.csv",
    "06_folio_count.csv",
    "07_scheme_performance.csv",
    "08_transactions.csv",
    "09_holdings.csv",
    "10_benchmark.csv"
]


def check_missing_files():
    """Checks if all 10 expected files exist in the data/raw/ directory."""
    status = {}
    missing_count = 0
    print("\nChecking raw datasets inside data/raw/...")
    
    for filename in EXPECTED_FILES:
        filepath = os.path.join(RAW_DATA_DIR, filename)
        exists = os.path.exists(filepath)
        status[filename] = exists
        if exists:
            print(f" [✔] Found: {filename}")
        else:
            print(f" [❌] Missing: {filename}")
            missing_count += 1
            
    if missing_count > 0:
        print(f"\n[!] Warning: {missing_count} out of {len(EXPECTED_FILES)} files are missing.")
        print("Please check that your raw CSV filenames match our list exactly.\n")
    else:
        print("\nAll 10 datasets are present! Continuing ingestion processing...\n")
        
    return status


def profile_datasets(file_status):
    """Task 3: Loads each present CSV, prints its shape, column data types, and head."""
    print("\n" + "="*70)
    print("TASK 3: Profiling and Loading the 10 CSV Datasets")
    print("="*70)
    
    for filename in EXPECTED_FILES:
        if not file_status.get(filename, False):
            continue
            
        filepath = os.path.join(RAW_DATA_DIR, filename)
        print(f"\n---> Profiling dataset: {filename}")
        
        try:
            df = pd.read_csv(filepath)
            print(f"     * Dimensions (Rows, Columns): {df.shape}")
            print("     * Column Data Types:")
            for col, dtype in df.dtypes.items():
                print(f"       - {col}: {dtype}")
            print("\n     * Sample Data (First 3 rows):")
            print(df.head(3))
            print("-" * 50)
        except Exception as e:
            print(f"     [!] Error profiling {filename}: {e}")


def explore_fund_master():
    """Task 6: Explores unique fields in '01_fund_master.csv'."""
    print("\n" + "="*70)
    print("TASK 6: Exploring Fund Master Metadata")
    print("="*70)
    
    filepath = os.path.join(RAW_DATA_DIR, "01_fund_master.csv")
    if not os.path.exists(filepath):
        print("[!] Cannot run Task 6 because '01_fund_master.csv' is missing.")
        return
        
    try:
        df = pd.read_csv(filepath)
        print(f"Available Columns: {df.columns.tolist()}")
        
        # Check specific columns
        if 'fund_house' in df.columns:
            print(f"\nUnique AMCs (Total: {df['fund_house'].nunique()}):")
            print(df['fund_house'].unique())
        if 'category' in df.columns:
            print(f"\nUnique Categories (Total: {df['category'].nunique()}):")
            print(df['category'].unique())
        if 'risk_category' in df.columns:
            print(f"\nUnique Risk Profiles (Total: {df['risk_category'].nunique()}):")
            print(df['risk_category'].unique())
            
    except Exception as e:
        print(f"[!] Error: {e}")


def validate_amfi_codes():
    """Task 7: Checks referential integrity between Master and History files."""
    print("\n" + "="*70)
    print("TASK 7: Validating AMFI Code Reference Integrity")
    print("="*70)
    
    master_path = os.path.join(RAW_DATA_DIR, "01_fund_master.csv")
    history_path = os.path.join(RAW_DATA_DIR, "02_nav_history.csv")
    
    if not os.path.exists(master_path) or not os.path.exists(history_path):
        print("[!] Cannot run Task 7. Both files must be present.")
        return
        
    try:
        df_master = pd.read_csv(master_path)
        df_history = pd.read_csv(history_path)
        
        master_codes = set(df_master['amfi_code'].astype(str).unique())
        history_codes = set(df_history['amfi_code'].astype(str).unique())
        
        print(f"Unique Scheme Codes in Master: {len(master_codes)}")
        print(f"Unique Scheme Codes in NAV History: {len(history_codes)}")
        
        unmatched_codes = master_codes - history_codes
        
        print("\n--- Data Quality Verification Summary ---")
        if len(unmatched_codes) == 0:
            print("✔ Referential Integrity PASS: Every scheme code in the Fund Master exists in the NAV History.")
        else:
            print(f"⚠ Referential Integrity WARNING: {len(unmatched_codes)} codes in Master are missing from History.")
            print(f"Missing codes sample: {list(unmatched_codes)[:5]}")
            
    except Exception as e:
        print(f"[!] Error: {e}")


def main():
    file_status = check_missing_files()
    profile_datasets(file_status)
    explore_fund_master()
    validate_amfi_codes()


if __name__ == "__main__":
    main()