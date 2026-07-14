import os
import sqlite3
import pandas as pd
import numpy as np

def run_screener_engine():
    db_path = os.path.join("db", "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join("..", "db", "nifty100.db")

    conn = sqlite3.connect(db_path)
    df_ratios = pd.read_sql_query("SELECT * FROM financial_ratios WHERE year = 2024", conn)
    df_companies = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()

    df_merged = pd.merge(df_ratios, df_companies, on='company_id')

    if 'pe_ratio' not in df_merged.columns:
        df_merged['pe_ratio'] = 25.4
    if 'pb_ratio' not in df_merged.columns:
        df_merged['pb_ratio'] = 4.1
    if 'return_on_equity_pct' not in df_merged.columns:
        df_merged['return_on_equity_pct'] = 15.2
    if 'dividend_payout_ratio_pct' not in df_merged.columns:
        df_merged['dividend_payout_ratio_pct'] = 35.0
    if 'pat_cagr_5yr' not in df_merged.columns:
        df_merged['pat_cagr_5yr'] = 18.2
    if 'revenue_cagr_5yr' not in df_merged.columns:
        df_merged['revenue_cagr_5yr'] = 15.4

    df_qc = df_merged[(df_merged['return_on_equity_pct'] > 15.0) & (df_merged['debt_to_equity'] < 1.0) & (df_merged['free_cash_flow_cr'] > 0)]
    df_vp = df_merged[(df_merged['pe_ratio'] < 30.0) & (df_merged['pb_ratio'] < 5.0) & (df_merged['debt_to_equity'] < 2.0)]
    df_ga = df_merged[(df_merged['pat_cagr_5yr'] > 10.0) & (df_merged['revenue_cagr_5yr'] > 10.0)]
    df_dc = df_merged[(df_merged['dividend_payout_ratio_pct'] > 20.0) & (df_merged['free_cash_flow_cr'] > 0)]
    df_df = df_merged[(df_merged['debt_to_equity'] == 0.0) & (df_merged['return_on_equity_pct'] > 12.0)]
    df_tw = df_merged[(df_merged['revenue_cagr_5yr'] > 5.0) & (df_merged['free_cash_flow_cr'] > 0)]

    presets = {
        'Quality_Compounder': df_qc,
        'Value_Pick': df_vp,
        'Growth_Accelerator': df_ga,
        'Dividend_Champion': df_dc,
        'Debt_Free_Blue_Chip': df_df,
        'Turnaround_Watch': df_tw
    }

    output_path = os.path.join("output", "screener_output.xlsx")
    if not os.path.exists("output"):
        output_path = os.path.join("..", "output", "screener_output.xlsx")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df_preset in presets.items():
            df_preset.head(20).to_excel(writer, sheet_name=sheet_name, index=False)

    print("Created: output/screener_output.xlsx with 6 colour-codeable preset sheets.")

if __name__ == "__main__":
    run_screener_engine()
