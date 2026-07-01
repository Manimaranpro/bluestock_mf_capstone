import pandas as pd
import unittest

from scripts.recommender import build_recommendations


class RecommenderTests(unittest.TestCase):
    def test_build_recommendations_ranks_low_risk_high_return_funds_first(self):
        sample = pd.DataFrame(
            [
                {
                    "amfi_code": "100001",
                    "scheme_name": "Stable Fund",
                    "sharpe_ratio": 0.9,
                    "alpha": 0.5,
                    "cagr_pct": 8.2,
                    "annual_volatility_pct": 6.0,
                    "max_drawdown_pct": -5.0,
                    "VaR_95": -0.010,
                    "CVaR_95": -0.014,
                },
                {
                    "amfi_code": "100002",
                    "scheme_name": "High Growth Fund",
                    "sharpe_ratio": 1.6,
                    "alpha": 1.2,
                    "cagr_pct": 16.5,
                    "annual_volatility_pct": 18.0,
                    "max_drawdown_pct": -20.0,
                    "VaR_95": -0.025,
                    "CVaR_95": -0.032,
                },
                {
                    "amfi_code": "100003",
                    "scheme_name": "Balanced Fund",
                    "sharpe_ratio": 1.3,
                    "alpha": 0.9,
                    "cagr_pct": 12.0,
                    "annual_volatility_pct": 10.2,
                    "max_drawdown_pct": -10.0,
                    "VaR_95": -0.015,
                    "CVaR_95": -0.019,
                },
            ]
        )

        result = build_recommendations(sample)

        self.assertIn("recommendation_score", result.columns)
        self.assertEqual(result.iloc[0]["scheme_name"], "Balanced Fund")
        self.assertTrue(result["recommendation_score"].is_monotonic_decreasing)


if __name__ == "__main__":
    unittest.main()
