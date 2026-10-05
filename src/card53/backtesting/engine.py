from __future__ import annotations

import pandas as pd


class BacktestEngine:
    def __init__(self, returns: pd.Series):
        self.returns = returns.copy().dropna()

    @property
    def cumulative_returns(self) -> pd.Series:
        return (1 + self.returns).cumprod()

    def equity_curve(self) -> pd.Series:
        return self.cumulative_returns
