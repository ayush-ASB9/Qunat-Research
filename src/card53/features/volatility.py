from __future__ import annotations

import numpy as np
import pandas as pd


def rolling_volatility(series: pd.Series, window: int = 20) -> pd.Series:
    returns = series.pct_change().dropna()
    return returns.rolling(window=window).std() * np.sqrt(252)


def realized_volatility(frame: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    data = frame.pct_change().dropna()
    return data.rolling(window=window).std() * np.sqrt(252)
