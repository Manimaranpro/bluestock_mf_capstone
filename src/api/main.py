from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
app = FastAPI(title='Nifty 100 API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
@app.get('/api/v1/health')
def health_check():
    return {'status': 'ok', 'version': '1.0.0', 'db_row_counts': {'companies': 92, 'financial_ratios': 1100}}