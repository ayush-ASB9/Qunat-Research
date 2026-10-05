from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
import yaml


def validate_iso_date(value: str, setting_name: str = "date") -> str:
    """Return a date string in YYYY-MM-DD form or raise a clear error."""
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError(f"{setting_name} must use YYYY-MM-DD format.")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise ValueError(f"{setting_name} must be a valid date in YYYY-MM-DD format.") from error


DEFAULT_CONFIG = {
    "project_name": "53rd Card",
    "market_universe": ["SPY", "QQQ", "IWM", "DIA", "VIX", "XLF", "XLK", "XLE"],
    "research_hypothesis": "The Invisible Player",
    "feature_window": 20,
    "lookback_days": 252,
    "volatility_regime_bins": 3,
    "min_valid_observations": 50,
}


@dataclass(frozen=True)
class Settings:
    project_name: str = "53rd Card"
    market_universe: list[str] = field(default_factory=lambda: DEFAULT_CONFIG["market_universe"].copy())
    research_hypothesis: str = "The Invisible Player"
    feature_window: int = 20
    lookback_days: int = 252
    volatility_regime_bins: int = 3
    min_valid_observations: int = 50
    default_start_date: str = "2010-01-01"
    default_end_date: str = field(default_factory=lambda: date.today().isoformat())
    data_dir: str = "data"
    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    results_dir: str = "results"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, config_path: str | Path | None = None) -> "Settings":
        if config_path is None:
            config_path = Path("config/research.yaml")
        config_path = Path(config_path)
        config_data = DEFAULT_CONFIG.copy()
        if config_path.exists():
            with config_path.open("r", encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle) or {}
            if isinstance(loaded, dict):
                config_data.update(loaded)

        load_dotenv()
        project_name = os.getenv("PROJECT_NAME", config_data.get("project_name", DEFAULT_CONFIG["project_name"]))
        market_universe = os.getenv("MARKET_UNIVERSE", ",".join(config_data.get("market_universe", DEFAULT_CONFIG["market_universe"])))
        universe = [symbol.strip() for symbol in market_universe.split(",") if symbol.strip()]
        start_date = os.getenv(
            "DEFAULT_START_DATE",
            str(config_data.get("default_start_date", "2010-01-01")),
        )
        configured_end_date = os.getenv("DEFAULT_END_DATE", config_data.get("default_end_date"))
        end_date = (
            date.today().isoformat()
            if configured_end_date is None
            else validate_iso_date(str(configured_end_date), "DEFAULT_END_DATE")
        )

        return cls(
            project_name=project_name,
            market_universe=universe or DEFAULT_CONFIG["market_universe"],
            research_hypothesis=os.getenv("RESEARCH_HYPOTHESIS", config_data.get("research_hypothesis", DEFAULT_CONFIG["research_hypothesis"])),
            feature_window=int(os.getenv("FEATURE_WINDOW", config_data.get("feature_window", DEFAULT_CONFIG["feature_window"]))),
            lookback_days=int(os.getenv("LOOKBACK_DAYS", config_data.get("lookback_days", DEFAULT_CONFIG["lookback_days"]))),
            volatility_regime_bins=int(os.getenv("VOLATILITY_REGIME_BINS", config_data.get("volatility_regime_bins", DEFAULT_CONFIG["volatility_regime_bins"]))),
            min_valid_observations=int(os.getenv("MIN_VALID_OBSERVATIONS", config_data.get("min_valid_observations", DEFAULT_CONFIG["min_valid_observations"]))),
            default_start_date=validate_iso_date(start_date, "DEFAULT_START_DATE"),
            default_end_date=end_date,
            data_dir=os.getenv("DATA_DIR", config_data.get("data_dir", "data")),
            raw_data_dir=os.getenv("RAW_DATA_DIR", config_data.get("raw_data_dir", "data/raw")),
            processed_data_dir=os.getenv("PROCESSED_DATA_DIR", config_data.get("processed_data_dir", "data/processed")),
            results_dir=os.getenv("RESULTS_DIR", config_data.get("results_dir", "results")),
            log_level=os.getenv("LOG_LEVEL", config_data.get("log_level", "INFO")),
        )


def load_settings(config_path: str | Path | None = None) -> Settings:
    return Settings.from_env(config_path=config_path)
