# Data Dictionary - Mutual Fund Analytics Database

## Tables & Schemas

### 1. dim_fund
Contains structural information about mutual fund schemes.
* `amfi_code` (INTEGER, Primary Key): Unique AMFI Identification Code.
* `fund_house` (TEXT): Name of the asset management company.
* `scheme_name` (TEXT): Name of the mutual fund scheme.
* `category` (TEXT): Broad classification (Equity, Debt, etc.).
* `sub_category` (TEXT): Sub-classification (Large Cap, Mid Cap, etc.).
* `plan` (TEXT): Plan Type (Regular, Direct).
* `launch_date` (TEXT): Date the scheme was launched.
* `benchmark` (TEXT): Target market index to compare returns.
* `risk_category` (TEXT): Risk profile assigned to the scheme.
* `sebi_category_code` (TEXT): Structural classification assigned by SEBI.

### 2. dim_date
A calendar dimension table used to simplify temporal analysis.
* `date` (TEXT, Primary Key): Calendar date (YYYY-MM-DD).
* `year` (INTEGER): Year component.
* `month` (INTEGER): Month component (1-12).
* `day` (INTEGER): Day of the month.
* `quarter` (INTEGER): Fiscal quarter.

### 3. fact_nav
Daily Net Asset Value (NAV) records.
* `amfi_code` (INTEGER, Foreign Key): Links to `dim_fund`.
* `date` (TEXT, Foreign Key): Links to `dim_date`.
* `nav` (REAL): Net Asset Value price of the day.

### 4. fact_transactions
Investor transaction records.
* `transaction_id` (TEXT, Primary Key): Unique transaction identifier.
* `amfi_code` (INTEGER, Foreign Key): Links to `dim_fund`.
* `date` (TEXT, Foreign Key): Links to `dim_date`.
* `transaction_type` (TEXT): SIP, Lumpsum, or Redemption.
* `amount` (REAL): Currency value of the transaction.
* `kyc_status` (TEXT): Investor KYC status.

### 5. fact_performance
Aggregated return history and cost ratios.
* `amfi_code` (INTEGER, Primary Key, Foreign Key): Links to `dim_fund`.
* `return_1yr` (REAL): Annual return percentage.
* `return_3yr` (REAL): 3-year annualized return percentage.
* `return_5yr` (REAL): 5-year annualized return percentage.
* `expense_ratio_pct` (REAL): Operating cost ratio.

### 6. fact_aum
Monthly Assets Under Management by fund house.
* `date` (TEXT, Foreign Key): Links to `dim_date`.
* `fund_house` (TEXT): Asset Management Company.
* `aum_crore` (REAL): Total value in Crores.
* `num_schemes` (INTEGER): Count of schemes contributing to AUM.
