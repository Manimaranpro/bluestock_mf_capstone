import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path

# Setup dynamic paths relative to this script to prevent hardcoding errors
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR = PROJECT_ROOT / "data" / "db"
SQL_DIR = PROJECT_ROOT / "sql"

# Ensure directories exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

def run_etl():
    print("--- Starting ETL Pipeline ---")
    
    # 1. Check database connectivity
    db_path = DB_DIR / "bluestock_mf.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"Connected to SQLite DB at: {db_path}")
    except Exception as e:
        print(f"Database connection error: {e}")
        sys.exit(1)
        
    # 2. Check for dynamic NAV fetch files or use raw templates
    nav_history_path = RAW_DIR / "02_nav_history.csv"
    fund_master_path = RAW_DIR / "01_fund_master.csv"
    
    if not nav_history_path.exists() or not fund_master_path.exists():
        print(f"Error: Essential raw CSV files missing from {RAW_DIR}")
        sys.exit(1)
        
    # 3. Clean and Preprocess NAV History (D1, D4)
    try:
        print("Processing NAV history (handling holiday and weekend gaps)...")
        df_nav = pd.read_csv(nav_history_path)
        
        # Verify columns from diagnostic data
        # ['amfi_code', 'date', 'nav']
        df_nav['date'] = pd.to_datetime(df_nav['date'])
        
        # Avoid duplicate dates per scheme
        df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
        
        # Reindexing and Forward-Filling NAV for Weekends/Holidays (Common Mistake Prevention)
        filled_dfs = []
        for amfi_code, group in df_nav.groupby('amfi_code'):
            group = group.set_index('date').sort_index()
            
            # Reindex to full date range
            full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
            group_reindexed = group.reindex(full_range)
            group_reindexed['amfi_code'] = amfi_code
            
            # Forward-fill missing NAV values
            group_reindexed['nav'] = group_reindexed['nav'].ffill()
            group_reindexed = group_reindexed.reset_index().rename(columns={'index': 'date'})
            filled_dfs.append(group_reindexed)
            
        df_nav_clean = pd.concat(filled_dfs, ignore_index=True)
        print(f"NAV History cleaned: {len(df_nav_clean)} records (fully filled).")
        
        # Save to processed directory
        df_nav_clean.to_csv(PROCESSED_DIR / "02_nav_history_cleaned.csv", index=False)
        df_nav_clean.to_sql("fact_nav", conn, if_exists="replace", index=False)
        print("fact_nav table loaded into database successfully.")
        
    except Exception as e:
        print(f"Error cleaning NAV history: {e}")
        sys.exit(1)

    # 4. Clean and Preprocess Fund Master
    try:
        df_master = pd.read_csv(fund_master_path)
        df_master.to_csv(PROCESSED_DIR / "01_fund_master_cleaned.csv", index=False)
        df_master.to_sql("dim_fund", conn, if_exists="replace", index=False)
        print("dim_fund table loaded into database successfully.")
    except Exception as e:
        print(f"Error cleaning fund master: {e}")
        sys.exit(1)

    # Close connection
    conn.commit()
    conn.close()
    print("--- ETL Pipeline Finished Successfully ---")

if __name__ == "__main__":
    run_etl()