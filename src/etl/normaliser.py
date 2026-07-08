import re

def normalize_year(year_val):
    if not year_val:
        return None
    val_str = str(year_val).strip()
    match = re.search(r'\b(20\d{2})\b', val_str)
    if match:
        return int(match.group(1))
    match_short = re.search(r'\b(\d{2})\b', val_str)
    if match_short:
        return 2000 + int(match_short.group(1))
    return None

def normalize_ticker(ticker_val):
    if not ticker_val:
        return None
    val_str = str(ticker_val).strip().upper()
    val_str = re.sub(r'^(NSE:|BSE:)', '', val_str)
    val_str = re.sub(r'(\.NS|\.BO)$', '', val_str)
    return val_str
