from __future__ import annotations

import pandas as pd

from card53.evaluation.statistics import pearson_correlation


def test_pearson_correlation():
    x = pd.Series([1.0, 2.0, 3.0, 4.0])
    y = pd.Series([2.0, 4.0, 6.0, 8.0])
    corr = pearson_correlation(x, y)
    assert corr == 1.0
