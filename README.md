# 53rd Card

53rd Card is a quantitative research project focused on US financial markets. The project is intentionally exploratory: it starts from a research question rather than a fixed trading idea, and it emphasizes disciplined data collection, feature engineering, testing, and falsification.

## Research question

The current working hypothesis is: "The Invisible Player." The project asks whether observable market variables can help infer latent or hidden market states such as changes in liquidity, volatility regime, participation, or market behavior, and whether transitions between such states contain statistically meaningful information about future market behavior.

This is not a claim that such states exist, that they are identifiable, or that they predict returns. The goal is to test whether any observed relationship survives rigorous statistical validation.

## Current market universe

The initial research universe is focused on major US listed assets, with a default set of broad-market and sector proxies such as:

- SPY
- QQQ
- IWM
- DIA
- VIX
- XLF
- XLK
- XLE

The project is designed to make the universe configurable through the settings file and environment variables so that experiments can expand, narrow, or change the asset list as needed.

## Project architecture

The repository is organized to separate research concerns, data handling, feature creation, testing, and evaluation:

- `config/` ? configuration and research defaults
- `data/` ? raw, processed, and external datasets
- `notebooks/` ? exploration and baseline analysis
- `research/` ? hypotheses, experiments, and retired ideas
- `src/card53/` ? reusable Python package
- `backtests/` ? backtesting documentation and notes
- `results/` ? figures, tables, and reports
- `scripts/` ? setup and project utilities
- `tests/` ? automated validation for core functionality

## Installation

This project targets Python 3.12+.

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the project dependencies.

Example:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scriptsctivate     # Windows PowerShell
pip install -r requirements-dev.txt
```

## Environment setup

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Then adjust the values to match your local environment. Do not commit `.env` files or any credentials or API keys.

The project reads settings from environment variables and a YAML config file so that collaborators can share reproducible defaults without embedding secrets.

## Typical workflow

1. Set up the environment.
2. Download market data.
3. Explore raw assets in notebooks.
4. Build features in `src/card53/features/`.
5. Write reproducible experiments in `research/`.
6. Run tests and validation.
7. Record results in `results/`.

## Research philosophy

This project follows a strict scientific workflow:

Hypothesis ? Data ? Feature ? Test ? Falsification ? Validation ? Out-of-sample test ? Paper trading

The goal is not to force a strategy to fit the data. The goal is to determine whether an effect survives careful testing.

## License

This project is licensed under the MIT License.
