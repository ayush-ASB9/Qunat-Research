from __future__ import annotations

import pandas as pd


def check_missing_values(frame: pd.DataFrame) -> pd.Series:
    return frame.isna().sum()


def check_duplicates(frame: pd.DataFrame) -> pd.Series:
    return frame.duplicated().sum()
