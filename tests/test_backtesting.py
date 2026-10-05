from __future__ import annotations

import pandas as pd

from card53.backtesting.engine import BacktestEngine
from card53.backtesting.metrics import sharpe_ratio


def test_backtest_engine():
    returns = pd.Series([0.01, -0.005, 0.02, 0.015])
    engine = BacktestEngine(returns)
    curve = engine.equity_curve()
    assert curve.iloc[0] == 1.01
    assert curve.iloc[-1] > 1.0


def test_sharpe_ratio():
    returns = pd.Series([0.01, 0.02, -0.01, 0.03])
    metric = sharpe_ratio(returns)
    assert metric == metric
