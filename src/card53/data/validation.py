from __future__ import annotations

import pandas as pd


def validate_market_data(frame: pd.DataFrame, required_columns: tuple[str, ...] = ("Close",)) -> pd.DataFrame:
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if frame.empty:
        raise ValueError("Market data is empty.")
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return frame.copy()
