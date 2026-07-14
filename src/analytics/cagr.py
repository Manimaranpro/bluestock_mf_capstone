def calculate_cagr(start, end, n):
    if n <= 0 or not start or not end:
        return None, "INSUFFICIENT"
    if start <= 0 and end <= 0:
        return None, "BOTH_NEGATIVE"
    if start <= 0 and end > 0:
        return None, "TURNAROUND"
    if start > 0 and end <= 0:
        return None, "DECLINE_TO_LOSS"
    if start == 0:
        return None, "ZERO_BASE"
    cagr = ((end / start) ** (1 / n) - 1) * 100
    return round(cagr, 2), "NORMAL"
