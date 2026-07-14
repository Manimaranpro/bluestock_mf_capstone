import pytest
from src.analytics.ratios import net_profit_margin_pct, debt_to_equity
from src.analytics.cagr import calculate_cagr

def test_np_margin():
    assert net_profit_margin_pct(1000, 10000) == 10.0
    assert net_profit_margin_pct(1000, 0) is None

def test_debt_equity():
    assert debt_to_equity(0, 100, 400) == 0.0
    assert debt_to_equity(500, 100, 400) == 1.0

def test_cagr_edge_cases():
    val, flag = calculate_cagr(100, 200, 3)
    assert flag == "NORMAL"
    val, flag = calculate_cagr(-50, 100, 3)
    assert flag == "TURNAROUND"
