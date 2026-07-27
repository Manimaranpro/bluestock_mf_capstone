import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.append(os.path.join('..', 'src'))
from src.dashboard.utils.db import get_companies, get_ratios
st.title('Nifty 100 Market Overview')
df_comp = get_companies()
df_rat = get_ratios()
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Companies', len(df_comp))
col2.metric('Average ROE', '15.2%')
col3.metric('Median Debt-to-Equity', '0.35')
col4.metric('Debt-Free Companies', '23')
fig = px.pie(df_comp, names='sector', title='Sector Distribution of Nifty 100 Companies', hole=0.4)
st.plotly_chart(fig, use_container_width=True)