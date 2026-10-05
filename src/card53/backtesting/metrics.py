from __future__ import annotations

import numpy as np
import pandas as pd


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    excess = returns - risk_free_rate / 252
    if excess.std(ddof=1) == 0:
        return 0.0
    return np.sqrt(252) * excess.mean() / excess.std(ddof=1)


def max_drawdown(values: pd.Series) -> float:
    running_max = values.cummax()
    drawdown = (values - running_max) / running_max
    return float(drawdown.min())
