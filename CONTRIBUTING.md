# Contributing to 53rd Card

Thank you for contributing to 53rd Card.

## Clone the repository

```bash
git clone <repository-url>
cd 53rd-card
```

## Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows PowerShell
```

## Install dependencies

```bash
pip install -r requirements-dev.txt
```

## Create your local environment file

```bash
cp .env.example .env
```

Do not commit credentials, tokens, or secrets. Keep `.env` local to your machine.

## Branching and collaboration

- Create a branch for meaningful work.
- Pull before starting work when your branch is behind `main`.
- Commit clearly and keep changes focused.
- Push updates to your own GitHub fork or repository remote.

## Research workflow

- Use notebooks for exploration and quick prototyping.
- Move reusable logic into `src/`.
- Document important experiments in the `research/` directories.
- Keep experiments reproducible and understandable.
- Avoid committing generated data or private credentials.

## Before opening a pull request

- Update relevant documentation when behavior changes.
- Run project tests.
- Confirm that the project still works from a clean checkout.
