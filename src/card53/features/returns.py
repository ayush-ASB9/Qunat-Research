from __future__ import annotations

import pandas as pd


def simple_returns(series: pd.Series) -> pd.Series:
    return series.pct_change().dropna()


def aligned_returns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.pct_change().dropna()
