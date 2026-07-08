-- Query 1: Validate company count equals 92
SELECT COUNT(*) AS total_companies FROM companies;

-- Query 2: Find top 5 companies by sales
SELECT c.company_name, p.year, p.sales 
FROM profitandloss p
JOIN companies c ON p.company_id = c.company_id
ORDER BY p.sales DESC
LIMIT 5;

-- Query 3: Check Balance Sheet Integrity Mismatches
SELECT company_id, year, total_assets, total_liabilities, abs(total_assets - total_liabilities) AS discrepancy
FROM balancesheet
WHERE abs(total_assets - total_liabilities) > 0;

-- Query 4: List companies with zero or negative sales
SELECT c.company_name, p.year, p.sales
FROM profitandloss p
JOIN companies c ON p.company_id = c.company_id
WHERE p.sales <= 0;

-- Query 5: Average operating cash flow by sector
SELECT sector, AVG(operating_cf) AS avg_ocf
FROM cashflow cf
JOIN companies c ON cf.company_id = c.company_id
GROUP BY sector;

-- Query 6: Year-on-year sales growth rate per company
SELECT company_id, year, sales,
       lag(sales) OVER (PARTITION BY company_id ORDER BY year) AS prev_sales
FROM profitandloss;

-- Query 7: List documents associated with high-ROE companies
SELECT c.company_name, r.roe_pct, d.doc_type, d.url
FROM financial_ratios r
JOIN companies c ON r.company_id = c.company_id
JOIN documents d ON c.company_id = d.company_id
WHERE r.roe_pct > 15.0;

-- Query 8: Peer comparison analysis
SELECT c.company_name, p.peer_1_ticker, p.peer_2_ticker
FROM peer_groups p
JOIN companies c ON p.company_id = c.company_id;

-- Query 9: Average close stock price per company
SELECT company_id, AVG(close_value) AS avg_price
FROM stock_prices
GROUP BY company_id;

-- Query 10: Find companies with operating loss
SELECT c.company_name, p.year, p.operating_profit
FROM profitandloss p
JOIN companies c ON p.company_id = c.company_id
WHERE p.operating_profit < 0;
