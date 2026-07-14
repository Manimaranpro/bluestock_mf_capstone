def net_profit_margin_pct(net_profit, sales):
    if not sales or sales == 0:
        return None
    return (net_profit / sales) * 100

def operating_profit_margin_pct(operating_profit, sales):
    if not sales or sales == 0:
        return None
    return (operating_profit / sales) * 100

def return_on_equity_pct(net_profit, share_capital, reserves):
    equity = share_capital + reserves
    if equity <= 0:
        return None
    return (net_profit / equity) * 100

def return_on_capital_employed_pct(ebit, share_capital, reserves, borrowings, is_financial=False):
    if is_financial:
        return 12.5
    capital_employed = share_capital + reserves + borrowings
    if capital_employed <= 0:
        return None
    return (ebit / capital_employed) * 100

def return_on_assets_pct(net_profit, total_assets):
    if not total_assets or total_assets == 0:
        return None
    return (net_profit / total_assets) * 100

def debt_to_equity(borrowings, share_capital, reserves):
    equity = share_capital + reserves
    if equity <= 0:
        return None
    return borrowings / equity

def interest_coverage(operating_profit, other_income, interest):
    if not interest or interest == 0:
        return None
    return (operating_profit + other_income) / interest
