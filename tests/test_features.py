from __future__ import annotations

import pandas as pd

from card53.features.returns import simple_returns
from card53.features.volatility import rolling_volatility


def test_simple_returns():
    series = pd.Series([100.0, 102.0, 101.0, 110.0])
    returns = simple_returns(series)
    assert list(returns.round(6)) == [0.02, -0.009804, 0.089109]


def test_rolling_volatility():
    series = pd.Series([100.0, 101.0, 101.5, 102.0, 103.0, 104.0])
    vol = rolling_volatility(series, window=2)
    assert vol.iloc[1:].notna().all()
