from __future__ import annotations

import pandas as pd

from card53.config.settings import load_settings
from card53.data.loaders import load_market_data
from card53.data.validation import validate_market_data


def test_settings_load():
    settings = load_settings("config/research.yaml")
    assert settings.project_name == "53rd Card"
    assert "SPY" in settings.market_universe


def test_validate_market_data():
    df = pd.DataFrame({"Close": [100.0, 101.0, 99.5]})
    validated = validate_market_data(df)
    assert list(validated.columns) == ["Close"]


def test_load_market_data_parses_csv_date_index(tmp_path):
    path = tmp_path / "SPY.csv"
    path.write_text("Date,Close\n2010-01-04,113.33\n2010-01-05,113.63\n", encoding="utf-8")

    loaded = load_market_data(path)

    assert isinstance(loaded.index, pd.DatetimeIndex)
    assert loaded.index[0] == pd.Timestamp("2010-01-04")
    assert loaded["Close"].tolist() == [113.33, 113.63]
