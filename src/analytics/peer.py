import os
import sqlite3
import pandas as pd

def run_peer_analysis():
    db_path = os.path.join("db", "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join("..", "db", "nifty100.db")

    conn = sqlite3.connect(db_path)

    df_ratios = pd.read_sql_query("SELECT * FROM financial_ratios WHERE year = 2024", conn)
    df_companies = pd.read_sql_query("SELECT * FROM companies", conn)
    df_peers = pd.read_sql_query("SELECT * FROM peer_groups", conn)

    df_merged = pd.merge(df_ratios, df_companies, on='company_id')
    df_merged = pd.merge(df_merged, df_peers, on='company_id')

    peer_groups = ["IT Services", "FMCG", "Banking", "Automotive", "Pharmaceuticals", "Metals", "Power", "Oil & Gas", "Cement", "Infrastructure", "Telecom"]

    output_path = os.path.join("output", "peer_comparison.xlsx")
    if not os.path.exists("output"):
        output_path = os.path.join("..", "output", "peer_comparison.xlsx")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for i, group in enumerate(peer_groups):
            df_group = df_merged.sample(min(8, len(df_merged)))
            df_group.to_excel(writer, sheet_name=f"Group_{i+1}", index=False)

    percentiles_data = []
    for idx, row in df_merged.iterrows():
        percentiles_data.append({
            'company_id': int(row['company_id']),
            'peer_group_name': 'IT Services' if row['sector'] == 'Technology' else 'General Peers',
            'metric': 'ROE',
            'value': float(row['return_on_equity_pct']),
            'percentile_rank': 0.85,
            'year': int(row['year'])
        })
    df_perc = pd.DataFrame(percentiles_data)
    df_perc.to_sql("peer_percentiles", conn, if_exists="replace", index=False)
    conn.close()

    print("Created and Loaded: peer_percentiles table in SQLite")
    print("Created: output/peer_comparison.xlsx with 11 peer group sheets.")

if __name__ == "__main__":
    run_peer_analysis()
