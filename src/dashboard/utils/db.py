import os
import sqlite3
import pandas as pd
import streamlit as st
def get_db_connection():
    db_path = os.path.join('db', 'nifty100.db')
    if not os.path.exists(db_path):
        db_path = os.path.join('..', 'db', 'nifty100.db')
    return sqlite3.connect(db_path)
@st.cache_data(ttl=600)
def get_companies():
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM companies', conn)
    conn.close()
    return df
@st.cache_data(ttl=600)
def get_ratios(ticker=None, year=None):
    conn = get_db_connection()
    query = 'SELECT r.*, c.ticker, c.company_name FROM financial_ratios r JOIN companies c ON r.company_id = c.company_id'
    if ticker:
        query += f" WHERE c.ticker = '{ticker}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_db_connection()
    df = pd.read_sql_query(f"SELECT p.* FROM profitandloss p JOIN companies c ON p.company_id = c.company_id WHERE c.ticker = '{ticker}'", conn)
    conn.close()
    return df
@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_db_connection()
    df = pd.read_sql_query(f"SELECT b.* FROM balancesheet b JOIN companies c ON b.company_id = c.company_id WHERE c.ticker = '{ticker}'", conn)
    conn.close()
    return df
@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_db_connection()
    df = pd.read_sql_query(f"SELECT cf.* FROM cashflow cf JOIN companies c ON cf.company_id = c.company_id WHERE c.ticker = '{ticker}'", conn)
    conn.close()
    return df