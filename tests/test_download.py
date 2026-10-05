from __future__ import annotations

from datetime import date

import pandas as pd
import pytest

from card53.config import settings as settings_module
from card53.config.settings import Settings
from card53.data import download as download_module
from scripts import download_data


class FixedDate(date):
    @classmethod
    def today(cls):
        return cls(2026, 10, 3)


def test_parser_reads_ticker_and_date_arguments():
    args = download_data.build_parser().parse_args(
        ["--ticker", "SPY,QQQ", "--start", "2010-01-01", "--end", "2026-10-03"]
    )

    assert args.ticker == "SPY,QQQ"
    assert args.start == "2010-01-01"
    assert args.end == "2026-10-03"


@pytest.mark.parametrize("value", ["today", "2010-1-1", "2010-02-30"])
def test_parser_rejects_invalid_dates(value):
    with pytest.raises(SystemExit) as error:
        download_data.build_parser().parse_args(["--start", value])

    assert error.value.code == 2


def test_settings_generate_valid_current_default_end_date(tmp_path, monkeypatch):
    monkeypatch.setattr(settings_module, "date", FixedDate)
    monkeypatch.delenv("DEFAULT_START_DATE", raising=False)
    monkeypatch.delenv("DEFAULT_END_DATE", raising=False)

    settings = Settings.from_env(tmp_path / "missing.yaml")

    assert settings.default_start_date == "2010-01-01"
    assert settings.default_end_date == "2026-10-03"


def test_settings_resolve_environment_over_config_over_defaults(tmp_path, monkeypatch):
    config_path = tmp_path / "research.yaml"
    config_path.write_text(
        "default_start_date: '2012-01-01'\ndefault_end_date: '2025-12-31'\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(settings_module, "date", FixedDate)
    monkeypatch.setenv("DEFAULT_START_DATE", "2014-01-01")
    monkeypatch.delenv("DEFAULT_END_DATE", raising=False)

    settings = Settings.from_env(config_path)

    assert settings.default_start_date == "2014-01-01"
    assert settings.default_end_date == "2025-12-31"


def test_settings_reject_invalid_configured_dates(tmp_path):
    config_path = tmp_path / "research.yaml"
    config_path.write_text("default_start_date: today\n", encoding="utf-8")

    with pytest.raises(ValueError, match="DEFAULT_START_DATE"):
        Settings.from_env(config_path)


def test_single_ticker_download_uses_valid_dates_sequentially(monkeypatch):
    columns = pd.MultiIndex.from_tuples([("Close", "SPY")])
    returned_data = pd.DataFrame([[500.0]], columns=columns)
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return returned_data

    monkeypatch.setattr(download_module.yf, "download", fake_download)

    result = download_module.download_market_data(
        "SPY", start="2010-01-01", end="2026-10-03"
    )

    assert result["Close"].tolist() == [500.0]
    assert calls[0]["tickers"] == "SPY"
    assert calls[0]["start"] == "2010-01-01"
    assert calls[0]["end"] == "2026-10-03"
    assert calls[0]["threads"] is False


def test_vix_alias_uses_yahoo_index_symbol(monkeypatch):
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return pd.DataFrame({"Close": [20.0]})

    monkeypatch.setattr(download_module.yf, "download", fake_download)

    download_module.download_market_data("VIX", start="2010-01-01", end="2026-10-03")

    assert calls[0]["tickers"] == "^VIX"
    assert calls[0]["threads"] is False


def test_download_api_generates_valid_default_end_date(monkeypatch):
    monkeypatch.setattr(download_module, "date", FixedDate)
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return pd.DataFrame({"Close": [500.0]})

    monkeypatch.setattr(download_module.yf, "download", fake_download)

    download_module.download_market_data("SPY", start="2010-01-01")

    assert calls[0]["end"] == "2026-10-03"


def test_cli_uses_only_selected_ticker_and_reports_partial_failure(tmp_path, monkeypatch, capsys):
    settings = Settings(raw_data_dir=str(tmp_path), market_universe=["SPY", "QQQ"])
    monkeypatch.setattr(download_data, "load_settings", lambda: settings)
    requested = []

    def fake_download(ticker, **kwargs):
        requested.append((ticker, kwargs))
        if ticker == "QQQ":
            raise RuntimeError("provider unavailable")
        return pd.DataFrame({"Close": [500.0, 501.0]})

    monkeypatch.setattr(download_data, "download_market_data", fake_download)

    result = download_data.main(
        ["--ticker", "SPY", "--start", "2010-01-01", "--end", "2026-10-03"]
    )
    output = capsys.readouterr().out

    assert result == 0
    assert [ticker for ticker, _ in requested] == ["SPY"]
    assert requested[0][1]["start"] == "2010-01-01"
    assert requested[0][1]["end"] == "2026-10-03"
    assert (tmp_path / "SPY.csv").exists()
    assert "SPY: SUCCESS - 2 rows" in output
    assert "Successful downloads: 1" in output
    assert "Failed downloads: 0" in output
    assert f"Output location: {tmp_path}" in output


def test_cli_defaults_to_configured_ticker_universe_and_continues_on_failure(
    tmp_path, monkeypatch, capsys
):
    tickers = ["SPY", "QQQ", "IWM"]
    settings = Settings(raw_data_dir=str(tmp_path), market_universe=tickers)
    monkeypatch.setattr(download_data, "load_settings", lambda: settings)
    requested = []

    def fake_download(ticker, **kwargs):
        requested.append((ticker, kwargs))
        if ticker == "QQQ":
            raise RuntimeError("database is locked")
        return pd.DataFrame({"Close": [100.0]})

    monkeypatch.setattr(download_data, "download_market_data", fake_download)

    result = download_data.main([])
    output = capsys.readouterr().out

    assert result == 1
    assert [ticker for ticker, _ in requested] == tickers
    assert requested[0][1]["start"] == settings.default_start_date
    assert requested[0][1]["end"] == settings.default_end_date
    assert (tmp_path / "SPY.csv").exists()
    assert not (tmp_path / "QQQ.csv").exists()
    assert (tmp_path / "IWM.csv").exists()
    assert "QQQ: FAILED - database is locked" in output
    assert "Successful downloads: 2" in output
    assert "Failed downloads: 1" in output
