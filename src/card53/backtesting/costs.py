from __future__ import annotations


def transaction_costs(trade_value: float, per_trade: float = 0.0005) -> float:
    return trade_value * per_trade
