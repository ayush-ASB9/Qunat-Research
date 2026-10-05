from __future__ import annotations

import pandas as pd


def moving_average(series: pd.Series, window: int = 20) -> pd.Series:
    return series.rolling(window=window).mean()


def relative_strength_index(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=window).mean()
    loss = (-delta.clip(upper=0)).rolling(window=window).mean()
    rs = gain / loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))
