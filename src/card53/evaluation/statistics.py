from __future__ import annotations

import numpy as np
import pandas as pd


def pearson_correlation(x: pd.Series, y: pd.Series) -> float:
    if x.empty or y.empty:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def summarize_distribution(series: pd.Series) -> dict[str, float]:
    return {
        "mean": float(series.mean()),
        "std": float(series.std(ddof=1)),
        "min": float(series.min()),
        "max": float(series.max()),
    }
