from __future__ import annotations

import argparse
from pathlib import Path

from card53.config.settings import load_settings, validate_iso_date
from card53.data.download import download_market_data, save_raw_data
from card53.data.validation import validate_market_data


def _date_argument(value: str) -> str:
    try:
        return validate_iso_date(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download daily market data to the raw data directory.")
    parser.add_argument(
        "--ticker",
        help="Ticker symbol or comma-separated symbols. Defaults to the configured market universe.",
    )
    parser.add_argument("--start", type=_date_argument, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("--end", type=_date_argument, help="End date in YYYY-MM-DD format.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        settings = load_settings()
    except (OSError, TypeError, ValueError) as error:
        parser.error(f"Invalid project settings: {error}")

    if args.ticker is None:
        tickers = [ticker.strip() for ticker in settings.market_universe if ticker.strip()]
    else:
        tickers = [ticker.strip() for ticker in args.ticker.split(",") if ticker.strip()]
        if not tickers:
            parser.error("--ticker must contain at least one ticker symbol.")

    start = args.start or settings.default_start_date
    end = args.end or settings.default_end_date
    if start > end:
        parser.error("--start must be on or before --end.")

    output_dir = Path(settings.raw_data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    successful = 0
    failed = 0

    for ticker in tickers:
        try:
            data = download_market_data(
                ticker,
                start=start,
                end=end,
                progress=True,
            )
            data = validate_market_data(data)
            save_raw_data(data, ticker, output_dir)
        except Exception as error:
            failed += 1
            print(f"{ticker}: FAILED - {error}")
            continue

        successful += 1
        print(f"{ticker}: SUCCESS - {len(data)} rows")

    print(f"Successful downloads: {successful}")
    print(f"Failed downloads: {failed}")
    print(f"Output location: {output_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
