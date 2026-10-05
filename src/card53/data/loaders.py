from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_market_data(file_path: str | Path) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, index_col=0, parse_dates=[0])
    if path.suffix.lower() in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file type for {path}")
