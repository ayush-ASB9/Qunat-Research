from __future__ import annotations

import pandas as pd


def volume_zscore(series: pd.Series, window: int = 20) -> pd.Series:
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    return (series - rolling_mean) / rolling_std
