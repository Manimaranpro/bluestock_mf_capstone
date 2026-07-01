import os
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "sharpe_ratio",
    "alpha",
    "cagr_pct",
    "annual_volatility_pct",
    "max_drawdown_pct",
    "VaR_95",
    "CVaR_95",
}


def build_recommendations(metrics_df: pd.DataFrame, risk_metric: str = "VaR_95", risk_tolerance: str = "balanced") -> pd.DataFrame:
    """Create a simple risk-adjusted ranking for mutual funds.

    The ranking combines return quality, risk-adjusted performance, and downside risk.
    It is intentionally lightweight so it can run without external ML libraries.
    """

    if metrics_df is None or metrics_df.empty:
        raise ValueError("metrics_df must be a non-empty DataFrame")

    df = metrics_df.copy()
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"metrics_df is missing required columns: {sorted(missing)}")

    if risk_metric not in df.columns:
        raise ValueError(f"risk_metric '{risk_metric}' not found in input data")

    risk_tolerance = risk_tolerance.lower()
    tolerance_weights = {
        "conservative": {"sharpe": 0.35, "alpha": 0.25, "cagr": 0.20, "vol": 0.15, "drawdown": 0.10, "risk": 0.10},
        "balanced": {"sharpe": 0.35, "alpha": 0.25, "cagr": 0.20, "vol": 0.15, "drawdown": 0.10, "risk": 0.10},
        "aggressive": {"sharpe": 0.40, "alpha": 0.30, "cagr": 0.25, "vol": 0.08, "drawdown": 0.05, "risk": 0.05},
    }

    if risk_tolerance not in tolerance_weights:
        raise ValueError(f"risk_tolerance must be one of: {sorted(tolerance_weights)}")

    weights = tolerance_weights[risk_tolerance]

    df["risk_penalty"] = df[risk_metric].abs().fillna(0) * 10
    df["cvar_penalty"] = df["CVaR_95"].abs().fillna(0) * 10
    df["vol_penalty"] = df["annual_volatility_pct"].fillna(0) / 10.0
    df["drawdown_penalty"] = df["max_drawdown_pct"].abs().fillna(0) / 10.0

    df["recommendation_score"] = (
        weights["sharpe"] * df["sharpe_ratio"].fillna(0)
        + weights["alpha"] * df["alpha"].fillna(0)
        + weights["cagr"] * (df["cagr_pct"].fillna(0) / 10.0)
        - weights["vol"] * df["vol_penalty"]
        - weights["drawdown"] * df["drawdown_penalty"]
        - weights["risk"] * (df["risk_penalty"] + df["cvar_penalty"])
    )

    return df.sort_values(by="recommendation_score", ascending=False).reset_index(drop=True)


def load_recommendation_inputs(base_dir: str | None = None) -> pd.DataFrame:
    base_path = Path(base_dir or Path(__file__).resolve().parent.parent)
    performance_path = base_path / "data" / "processed" / "07_scheme_performance_cleaned.csv"
    risk_path = base_path / "data" / "processed" / "var_cvar_report.csv"

    performance_df = pd.read_csv(performance_path)
    risk_df = pd.read_csv(risk_path)

    merged = performance_df.merge(risk_df, on="amfi_code", how="left")
    return merged


def generate_recommendations(output_path: str | None = None, risk_tolerance: str = "balanced") -> pd.DataFrame:
    merged_df = load_recommendation_inputs()
    ranked = build_recommendations(merged_df, risk_tolerance=risk_tolerance)

    if output_path is None:
        output_path = os.path.join("data", "processed", "ai_recommendations.csv")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(output_file, index=False)
    return ranked


if __name__ == "__main__":
    recommendations = generate_recommendations()
    print(recommendations[["scheme_name", "recommendation_score", "sharpe_ratio", "alpha", "cagr_pct", "annual_volatility_pct", "VaR_95"]].head(10))
