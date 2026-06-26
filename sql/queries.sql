SELECT fund_house, MAX(aum_crore) AS max_aum 
FROM fact_aum 
GROUP BY fund_house 
ORDER BY max_aum DESC 
LIMIT 5;

SELECT amfi_code, strftime('%Y-%m', date) AS month, AVG(nav) AS avg_nav 
FROM fact_nav 
GROUP BY amfi_code, month;

SELECT transaction_type, SUM(amount) AS total_amount 
FROM fact_transactions 
GROUP BY transaction_type;

SELECT kyc_status, COUNT(*) AS txn_count 
FROM fact_transactions 
GROUP BY kyc_status;

SELECT amfi_code, expense_ratio_pct 
FROM fact_performance 
WHERE expense_ratio_pct < 1.0;

SELECT f.category, AVG(p.return_3yr) AS avg_3yr_return 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.category;

SELECT fund_house, COUNT(amfi_code) AS scheme_count 
FROM dim_fund 
GROUP BY fund_house 
HAVING scheme_count > 3;

SELECT amfi_code, MAX(nav) AS max_nav, MIN(nav) AS min_nav 
FROM fact_nav 
GROUP BY amfi_code;

SELECT strftime('%Y-%m', date) AS month, COUNT(*) AS transaction_count 
FROM fact_transactions 
GROUP BY month 
ORDER BY month;

SELECT f.scheme_name, f.risk_category, p.return_5yr 
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE f.risk_category = 'Very High' 
ORDER BY p.return_5yr DESC;