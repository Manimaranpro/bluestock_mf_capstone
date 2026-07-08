import pandas as pd
import numpy as np

def run_dq_validation(dfs):
    failures = []
    df_c = dfs['companies']
    if df_c['ticker'].duplicated().any():
        dupes = df_c[df_c['ticker'].duplicated()]['ticker'].tolist()
        for d in dupes:
            failures.append({'rule_id': 'DQ-01', 'table': 'companies', 'key': d, 'severity': 'CRITICAL', 'msg': 'Duplicate ticker'})
    df_pl = dfs['profitandloss']
    if df_pl.duplicated(subset=['company_id', 'year']).any():
        failures.append({'rule_id': 'DQ-02', 'table': 'profitandloss', 'key': 'multiple', 'severity': 'CRITICAL', 'msg': 'Duplicate compound PK'})
    df_bs = dfs['balancesheet']
    for idx, row in df_bs.iterrows():
        diff = abs(row['total_assets'] - row['total_liabilities'])
        if row['total_assets'] > 0 and (diff / row['total_assets']) > 0.01:
            failures.append({'rule_id': 'DQ-04', 'table': 'balancesheet', 'key': f"{row['company_id']}_{row['year']}", 'severity': 'WARNING', 'msg': 'BS mismatch'})
    for idx, row in df_pl.iterrows():
        if row['sales'] > 0:
            calc_opm = (row['operating_profit'] / row['sales']) * 100
            if abs(calc_opm - row['opm_pct']) > 2.0:
                failures.append({'rule_id': 'DQ-05', 'table': 'profitandloss', 'key': f"{row['company_id']}_{row['year']}", 'severity': 'WARNING', 'msg': 'OPM mismatch'})
    for idx, row in df_pl.iterrows():
        if row['sales'] <= 0:
            failures.append({'rule_id': 'DQ-06', 'table': 'profitandloss', 'key': f"{row['company_id']}_{row['year']}", 'severity': 'WARNING', 'msg': 'Sales <= 0'})
    return pd.DataFrame(failures)
