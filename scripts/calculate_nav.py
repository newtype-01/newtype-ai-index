#!/usr/bin/env python3
"""Calculate newtype AI Index NAV vs benchmarks.

Reads:
  - data/constituents/<latest>.json (current index weights)
  - data/prices/close_prices.csv (daily close for constituents + benchmarks)

Writes:
  - data/nav/daily.csv (NTAI daily NAV)
  - data/nav/monthly.csv (NTAI month-end NAV)
  - data/benchmarks/comparison.csv (NTAI vs SOXX vs QQQ, all rebased to 100 at inception)

Standard library only, plus optional matplotlib (used by generate_chart.py, not here).

Rules:
  - Base date is the last trading day on or before the initial constituents file date.
  - Weights are fixed-target with monthly rebalance on the first trading day of each month.
    (Buy-and-hold drift is intentionally suppressed to reflect target-weight tracking.)
  - Any constituent change requires a new file in data/constituents/ dated on the effective date.
    The script picks the most recent constituents file with date <= current date.
"""
from __future__ import annotations

import csv
import json
import os
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONSTITUENTS_DIR = ROOT / "data" / "constituents"
PRICES_FILE = ROOT / "data" / "prices" / "close_prices.csv"
NAV_DIR = ROOT / "data" / "nav"
BENCH_DIR = ROOT / "data" / "benchmarks"
BENCH_TICKERS = ("SOXX", "QQQ")
BASE_NAV = 100.0000


def load_prices(path: Path) -> tuple[list[date], dict[str, dict[date, float]]]:
    """Return (sorted_dates, {ticker: {date: close}})."""
    rows: dict[str, dict[date, float]] = {}
    dates: set[date] = set()
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = datetime.strptime(row["date"], "%Y-%m-%d").date()
            t = row["ticker"]
            c = float(row["close"])
            rows.setdefault(t, {})[d] = c
            dates.add(d)
    return sorted(dates), rows


def load_constituents_history() -> list[tuple[date, dict]]:
    """Load all constituents files, sorted by effective date."""
    files = sorted(CONSTITUENTS_DIR.glob("*.json"))
    history = []
    for f in files:
        with f.open() as fh:
            data = json.load(fh)
        eff = datetime.strptime(data["meta"]["effective_date"], "%Y-%m-%d").date()
        history.append((eff, data))
    return history


def active_constituents(history: list[tuple[date, dict]], on: date) -> dict:
    """Return the constituents file active on the given date."""
    active = None
    for eff, data in history:
        if eff <= on:
            active = data
    if active is None:
        raise ValueError(f"No constituents file effective on or before {on}")
    return active


def calculate_nav(
    dates: list[date],
    prices: dict[str, dict[date, float]],
    history: list[tuple[date, dict]],
) -> list[tuple[date, float]]:
    """Compute NTAI daily NAV with monthly rebalance to target weights.

    Method: on rebalance day (first trading day of each calendar month, and inception),
    reset each constituent's share count so that its dollar value equals target_weight * NAV.
    Between rebalances, hold share counts constant (buy-and-hold within the month).
    """
    if not dates:
        return []

    # Inception is the first available trading date
    inception = dates[0]
    active = active_constituents(history, inception)
    tickers = [c["ticker"] for c in active["constituents"]]
    weights = {c["ticker"]: c["weight"] for c in active["constituents"]}

    # Verify all constituents have price data on inception
    for t in tickers:
        if inception not in prices.get(t, {}):
            raise ValueError(f"{t} has no price on inception {inception}")

    # Initial share allocation to match target weights at NAV=100
    nav = BASE_NAV
    shares = {}
    for t in tickers:
        p0 = prices[t][inception]
        shares[t] = (weights[t] * nav) / p0

    nav_series: list[tuple[date, float]] = []
    prev_month = inception.month
    prev_year = inception.year

    for d in dates:
        # Refresh active constituents if a new file becomes effective
        current_active = active_constituents(history, d)
        if current_active is not active:
            active = current_active
            tickers = [c["ticker"] for c in active["constituents"]]
            weights = {c["ticker"]: c["weight"] for c in active["constituents"]}
            # Rebalance immediately using previous NAV
            # First compute current NAV using prior shares & prior tickers
            # (only if any shared tickers still exist)
            prior_shares = shares
            # Value the portfolio at today's prices using the OLD holdings
            # (all prior tickers should still have prices)
            old_nav = sum(prior_shares.get(t, 0) * prices[t].get(d, 0) for t in prior_shares)
            if old_nav > 0:
                nav = old_nav
            shares = {t: (weights[t] * nav) / prices[t][d] for t in tickers}

        # Monthly rebalance on first trading day of each month (except inception, already set)
        if d != inception and (d.month != prev_month or d.year != prev_year):
            # Value portfolio at today's prices with prior shares
            nav = sum(shares[t] * prices[t][d] for t in tickers)
            shares = {t: (weights[t] * nav) / prices[t][d] for t in tickers}

        # Daily NAV
        nav_today = sum(shares[t] * prices[t][d] for t in tickers)
        nav_series.append((d, nav_today))

        prev_month = d.month
        prev_year = d.year

    return nav_series


def rebase_series(dates: list[date], prices: dict[date, float]) -> list[tuple[date, float]]:
    """Rebase a price series so the first date equals BASE_NAV."""
    if not dates:
        return []
    p0 = prices[dates[0]]
    return [(d, BASE_NAV * prices[d] / p0) for d in dates]


def month_ends(nav: list[tuple[date, float]]) -> list[tuple[date, float]]:
    """Return the last data point of each calendar month."""
    if not nav:
        return []
    out = []
    for i, (d, v) in enumerate(nav):
        is_last = i == len(nav) - 1 or nav[i + 1][0].month != d.month
        if is_last:
            out.append((d, v))
    return out


def write_csv(path: Path, header: list[str], rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main() -> None:
    if not PRICES_FILE.exists():
        raise SystemExit(
            f"Prices file not found: {PRICES_FILE}\n"
            "Populate data/prices/close_prices.csv (columns: date,ticker,close) before running."
        )

    dates, prices = load_prices(PRICES_FILE)
    history = load_constituents_history()

    ntai = calculate_nav(dates, prices, history)

    # Write daily NAV
    write_csv(
        NAV_DIR / "daily.csv",
        ["date", "ntai_nav"],
        [[d.isoformat(), f"{v:.4f}"] for d, v in ntai],
    )

    # Write monthly NAV
    monthly = month_ends(ntai)
    write_csv(
        NAV_DIR / "monthly.csv",
        ["date", "ntai_nav"],
        [[d.isoformat(), f"{v:.4f}"] for d, v in monthly],
    )

    # Rebase benchmarks
    soxx_rebased = rebase_series(dates, prices["SOXX"])
    qqq_rebased = rebase_series(dates, prices["QQQ"])

    ntai_map = dict(ntai)
    soxx_map = dict(soxx_rebased)
    qqq_map = dict(qqq_rebased)

    rows = []
    for d in dates:
        rows.append(
            [
                d.isoformat(),
                f"{ntai_map[d]:.4f}",
                f"{soxx_map[d]:.4f}",
                f"{qqq_map[d]:.4f}",
            ]
        )
    write_csv(
        BENCH_DIR / "comparison.csv",
        ["date", "ntai", "soxx", "qqq"],
        rows,
    )

    # Print summary
    inception = dates[0]
    latest = dates[-1]
    print(f"Inception:     {inception.isoformat()}  NAV = {ntai_map[inception]:.4f}")
    print(f"Latest:        {latest.isoformat()}  NAV = {ntai_map[latest]:.4f}")
    print(f"NTAI return:   {(ntai_map[latest] / BASE_NAV - 1) * 100:+.2f}%")
    print(f"SOXX return:   {(soxx_map[latest] / BASE_NAV - 1) * 100:+.2f}%")
    print(f"QQQ  return:   {(qqq_map[latest] / BASE_NAV - 1) * 100:+.2f}%")


if __name__ == "__main__":
    main()
