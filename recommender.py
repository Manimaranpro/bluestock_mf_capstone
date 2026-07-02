import pandas as pd
import numpy as np

try:
    df_score = pd.read_csv("data/processed/fund_scorecard.csv")
except:
    df_score = pd.read_csv("fund_scorecard.csv")

risk_mapping = {
    'Low': ['Low', 'Moderate'],
    'Moderate': ['Moderate', 'Moderately High', 'High'],
    'High': ['High', 'Very High']
}

print("=== Mutual Fund Recommender Engine ===")
risk_appetite = input("Enter your risk appetite (Low / Moderate / High): ").strip().title()

if risk_appetite in risk_mapping:
    matched_risk_grades = risk_mapping[risk_appetite]
    df_filtered = df_score[df_score['category'].isin(matched_risk_grades) | df_score['category'].str.contains('Debt|Liquid', case=False, na=False)] if risk_appetite == 'Low' else df_score
    df_rec = df_filtered.sort_values('sharpe_ratio', ascending=False).head(3)
    print("\nRecommended Top 3 Funds for you:")
    print(df_rec[['scheme_name', 'category', 'sharpe_ratio', 'composite_score']].to_string(index=False))
else:
    print("Invalid input. Please choose from Low, Moderate, or High.")
