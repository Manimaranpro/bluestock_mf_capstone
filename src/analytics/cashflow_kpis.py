def free_cash_flow(operating, investing):
    return operating + investing

def cfo_quality_score(cfo, pat):
    if not pat or pat == 0:
        return None, "Accrual Risk"
    ratio = cfo / pat
    if ratio > 1.0:
        return round(ratio, 2), "High Quality"
    elif 0.5 <= ratio <= 1.0:
        return round(ratio, 2), "Moderate"
    else:
        return round(ratio, 2), "Accrual Risk"

def capex_intensity(investing, sales):
    if not sales or sales == 0:
        return None, "Asset Light"
    ratio = (abs(investing) / sales) * 100
    if ratio < 3.0:
        return round(ratio, 2), "Asset Light"
    elif 3.0 <= ratio <= 8.0:
        return round(ratio, 2), "Moderate"
    else:
        return round(ratio, 2), "Capital Intensive"

def fcf_conversion_rate(fcf, operating_profit):
    if not operating_profit or operating_profit == 0:
        return None
    return (fcf / operating_profit) * 100

def capital_allocation_classifier(cfo, cfi, cff, pat):
    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    if cfo_sign == "+" and cfi_sign == "-" and cff_sign == "-":
        if pat > 0 and (cfo / pat) > 1.2:
            return "Shareholder Returns"
        return "Reinvestor"
    if cfo_sign == "+" and cfi_sign == "+" and cff_sign == "-":
        return "Liquidating Assets"
    if cfo_sign == "-" and cfi_sign == "+" and cff_sign == "+":
        return "Distress Signal"
    if cfo_sign == "-" and cfi_sign == "-" and cff_sign == "+":
        return "Growth Funded by Debt"
    if cfo_sign == "+" and cfi_sign == "+" and cff_sign == "+":
        return "Cash Accumulator"
    if cfo_sign == "-" and cfi_sign == "-" and cff_sign == "-":
        return "Pre-Revenue"
    return "Mixed"
