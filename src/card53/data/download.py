from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf


def _yahoo_symbol(symbol: str) -> str:
    """Translate the project's VIX alias to Yahoo Finance's index ticker."""
    return "^VIX" if symbol.upper() == "VIX" else symbol


def _validate_date(value: str, name: str) -> str:
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError(f"{name} must use YYYY-MM-DD format.")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise ValueError(f"{name} must be a valid date in YYYY-MM-DD format.") from error


def _single_ticker_frame(data: pd.DataFrame, yahoo_symbol: str) -> pd.DataFrame:
    if isinstance(data.columns, pd.MultiIndex):
        for level in range(data.columns.nlevels):
            if yahoo_symbol in data.columns.get_level_values(level):
                data = data.xs(yahoo_symbol, axis=1, level=level)
                break
        else:
            raise ValueError(f"Could not identify downloaded columns for {yahoo_symbol}.")
    return data


def download_market_data(
    symbols: str | list[str],
    start: str = "2010-01-01",
    end: str | None = None,
    interval: str = "1d",
    progress: bool = False,
) -> pd.DataFrame:
    """Download market data without yfinance's concurrent ticker workers."""
    if end is None:
        end = date.today().isoformat()
    start = _validate_date(start, "start")
    end = _validate_date(end, "end")
    if start > end:
        raise ValueError("start must be on or before end.")
    if isinstance(symbols, str):
        symbols = [symbols]
    if not symbols:
        raise ValueError("At least one ticker symbol is required.")

    yahoo_symbols = [_yahoo_symbol(symbol) for symbol in symbols]
    data = yf.download(
        tickers=yahoo_symbols[0] if len(yahoo_symbols) == 1 else yahoo_symbols,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=progress,
        group_by="ticker",
        threads=False,
    )
    if len(symbols) == 1:
        data = _single_ticker_frame(data, yahoo_symbols[0])
    return data


def save_raw_data(frame: pd.DataFrame, symbol: str, output_dir: str | Path = "data/raw") -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / f"{symbol}.csv"
    frame.to_csv(file_path)
    return file_path
