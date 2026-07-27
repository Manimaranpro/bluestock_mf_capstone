import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.append(os.path.join('..', 'src'))
from src.dashboard.utils.db import get_companies, get_pl
st.title('Company Profile & Performance Analysis')
df_comp = get_companies()
ticker = st.selectbox('Select a Ticker to Analyze', df_comp['ticker'].tolist())
df_pl = get_pl(ticker)
if not df_pl.empty:
    fig = px.bar(df_pl, x='year', y='sales', title=f'Historical Sales Trend for {ticker}', labels={'sales': 'Sales (in Crores)'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning('No financial data found for this company.')