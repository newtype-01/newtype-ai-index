#!/usr/bin/env python3
"""Fetch latest close prices from yfinance and append to data/prices/close_prices.csv.

Idempotent: only appends rows whose (date, ticker) pair is not already present.

Reads:
  - data/constituents/*.json (all constituent tickers)
  - data/prices/close_prices.csv (existing rows)

Writes:
  - data/prices/close_prices.csv (with new rows appended, sorted by ticker then date)

Data source: yfinance (Yahoo Finance). Benchmarks SOXX and QQQ are always included.
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
CONSTITUENTS_DIR = ROOT / "data" / "constituents"
PRICES_FILE = ROOT / "data" / "prices" / "close_prices.csv"
BENCHMARKS = ["SOXX", "QQQ"]


def collect_all_tickers() -> list[str]:
    """Union of all tickers ever appearing in any constituents file, plus benchmarks."""
    tickers: set[str] = set(BENCHMARKS)
    for f in CONSTITUENTS_DIR.glob("*.json"):
        with f.open() as fh:
            data = json.load(fh)
        for c in data.get("constituents", []):
            tickers.add(c["ticker"])
    return sorted(tickers)


def load_existing() -> tuple[dict[str, dict[date, float]], date | None]:
    """Return existing (ticker -> {date: close}) and the max date across all rows."""
    existing: dict[str, dict[date, float]] = {}
    max_date: date | None = None
    if not PRICES_FILE.exists():
        return existing, None
    with PRICES_FILE.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = datetime.strptime(row["date"], "%Y-%m-%d").date()
            t = row["ticker"]
            c = float(row["close"])
            existing.setdefault(t, {})[d] = c
            if max_date is None or d > max_date:
                max_date = d
    return existing, max_date


def fetch_ticker(ticker: str, start: date, end: date) -> dict[date, float]:
    """Return {date: close} for the ticker over [start, end] inclusive."""
    # yfinance end is exclusive, so add one day
    df = yf.download(
        ticker,
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        progress=False,
        auto_adjust=False,
    )
    if df.empty:
        return {}
    result: dict[date, float] = {}
    # yfinance may return a MultiIndex column ("Close", ticker)
    if isinstance(df.columns, __import__("pandas").MultiIndex):
        close_series = df["Close"][ticker]
    else:
        close_series = df["Close"]
    for idx, val in close_series.items():
        d = idx.date() if hasattr(idx, "date") else idx
        result[d] = float(val)
    return result


def write_prices(all_rows: dict[str, dict[date, float]]) -> None:
    """Write full CSV sorted by (date, ticker)."""
    rows = []
    for t in sorted(all_rows.keys()):
        for d in sorted(all_rows[t].keys()):
            rows.append([d.isoformat(), t, f"{all_rows[t][d]:.2f}"])
    PRICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PRICES_FILE.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "ticker", "close"])
        # Sort by date then ticker for stable diffs
        rows.sort(key=lambda r: (r[0], r[1]))
        w.writerows(rows)


def main() -> int:
    tickers = collect_all_tickers()
    existing, max_date = load_existing()

    today = date.today()
    # Start fetch from the day after max_date, or a reasonable default
    if max_date is None:
        start = date(2026, 7, 15)
    else:
        start = max_date + timedelta(days=1)

    if start > today:
        print(f"Already up to date (latest row: {max_date}).")
        return 0

    print(f"Fetching {len(tickers)} tickers from {start} to {today}...")
    added = 0
    for t in tickers:
        new_data = fetch_ticker(t, start, today)
        for d, c in new_data.items():
            if d in existing.get(t, {}):
                continue
            existing.setdefault(t, {})[d] = c
            added += 1

    if added == 0:
        print("No new rows to add (market may be closed or data not yet available).")
        return 0

    write_prices(existing)
    print(f"Added {added} new price rows across {len(tickers)} tickers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
