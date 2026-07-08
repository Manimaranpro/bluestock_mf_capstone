import pytest
from src.etl.normaliser import normalize_year, normalize_ticker

def test_normalize_year():
    assert normalize_year("FY 2023") == 2023
    assert normalize_year("2023-24") == 2023
    assert normalize_year("Mar-23") == 2023
    assert normalize_year(2023) == 2023

def test_normalize_ticker():
    assert normalize_ticker("NSE:RELIANCE") == "RELIANCE"
    assert normalize_ticker("TCS.NS") == "TCS"
    assert normalize_ticker("infy") == "INFY"
