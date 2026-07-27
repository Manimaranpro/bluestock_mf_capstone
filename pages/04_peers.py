import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.join('..', 'src'))
from src.dashboard.utils.db import get_companies
st.title('Peer Comparison Analysis')
df_comp = get_companies()
st.write('Successfully connected to the database. Exploring company sector weights and trends.')
st.dataframe(df_comp.head(10))