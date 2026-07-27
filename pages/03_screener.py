import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.join('..', 'src'))
from src.dashboard.utils.db import get_ratios
st.title('Interactive Stock Screener')
df_rat = get_ratios()
min_roe = st.sidebar.slider('Minimum ROE (%)', 0.0, 50.0, 15.0)
max_de = st.sidebar.slider('Maximum Debt-to-Equity', 0.0, 5.0, 1.0)
df_filtered = df_rat[(df_rat['return_on_equity_pct'] >= min_roe) & (df_rat['debt_to_equity'] <= max_de)]
st.write(f'### Screened Results ({len(df_filtered)} companies match filters)')
st.dataframe(df_filtered[['ticker', 'company_name', 'year', 'return_on_equity_pct', 'debt_to_equity']])
csv = df_filtered.to_csv(index=False)
st.download_button('Download Screened Data as CSV', csv, 'screened_results.csv', 'text/csv')