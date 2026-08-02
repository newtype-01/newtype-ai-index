#!/usr/bin/env python3
"""Export NAV data as JSON for consumption by frontend clients (e.g. website).

Reads:
  - data/benchmarks/comparison.csv (rebased NTAI vs SOXX vs QQQ)
  - data/nav/daily.csv (NTAI daily NAV)
  - data/constituents/<latest>.json (current constituents)

Writes:
  - data/api/latest.json (headline numbers + full time series)
  - data/api/constituents.json (current effective constituents)

These files are served via raw.githubusercontent.com and can be fetched
directly by static HTML pages using fetch().
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPARISON = ROOT / "data" / "benchmarks" / "comparison.csv"
DAILY_NAV = ROOT / "data" / "nav" / "daily.csv"
CONSTITUENTS_DIR = ROOT / "data" / "constituents"
PRICES_FILE = ROOT / "data" / "prices" / "close_prices.csv"
API_DIR = ROOT / "data" / "api"

BASE_NAV = 100.0


def load_prices() -> tuple[list[str], dict[str, dict[str, float]]]:
    """Return (sorted_date_strings, {ticker: {date_str: close}})."""
    prices: dict[str, dict[str, float]] = {}
    dates: set[str] = set()
    if not PRICES_FILE.exists():
        return [], {}
    with PRICES_FILE.open() as f:
        for row in csv.DictReader(f):
            d, t, c = row["date"], row["ticker"], float(row["close"])
            prices.setdefault(t, {})[d] = c
            dates.add(d)
    return sorted(dates), prices


def load_comparison() -> list[dict]:
    rows = []
    with COMPARISON.open() as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "date": row["date"],
                    "ntai": float(row["ntai"]),
                    "soxx": float(row["soxx"]),
                    "qqq": float(row["qqq"]),
                }
            )
    return rows


def latest_constituents_file() -> Path:
    files = sorted(CONSTITUENTS_DIR.glob("*.json"))
    if not files:
        raise SystemExit("No constituents files found")
    return files[-1]


def main() -> None:
    series = load_comparison()
    if not series:
        raise SystemExit("comparison.csv is empty")

    first = series[0]
    last = series[-1]

    latest = {
        "index_name": "newtype AI Index",
        "index_ticker": "NTAI",
        "inception_date": first["date"],
        "base_nav": BASE_NAV,
        "latest_date": last["date"],
        "latest_nav": round(last["ntai"], 4),
        "period_return_pct": round((last["ntai"] / BASE_NAV - 1) * 100, 2),
        "benchmarks": {
            "SOXX": {
                "latest": round(last["soxx"], 4),
                "period_return_pct": round((last["soxx"] / BASE_NAV - 1) * 100, 2),
                "excess_pp": round(
                    (last["ntai"] / BASE_NAV - 1) * 100
                    - (last["soxx"] / BASE_NAV - 1) * 100,
                    2,
                ),
            },
            "QQQ": {
                "latest": round(last["qqq"], 4),
                "period_return_pct": round((last["qqq"] / BASE_NAV - 1) * 100, 2),
                "excess_pp": round(
                    (last["ntai"] / BASE_NAV - 1) * 100
                    - (last["qqq"] / BASE_NAV - 1) * 100,
                    2,
                ),
            },
        },
        "series": series,
        "updated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://github.com/newtype-01/newtype-ai-index",
        "disclaimer": "Research-only. Not investment advice. Weights are model targets, not actual holdings.",
    }

    API_DIR.mkdir(parents=True, exist_ok=True)
    with (API_DIR / "latest.json").open("w") as f:
        json.dump(latest, f, indent=2, ensure_ascii=False)

    # Export current constituents, enriched with latest price + daily change
    with latest_constituents_file().open() as f:
        constituents = json.load(f)

    dates, prices = load_prices()
    if dates:
        latest_price_date = dates[-1]
        prev_price_date = dates[-2] if len(dates) >= 2 else None
        constituents["price_snapshot"] = {
            "latest_date": latest_price_date,
            "prev_date": prev_price_date,
        }
        for c in constituents.get("constituents", []):
            t = c["ticker"]
            latest_px = prices.get(t, {}).get(latest_price_date)
            prev_px = prices.get(t, {}).get(prev_price_date) if prev_price_date else None
            c["latest_price"] = round(latest_px, 2) if latest_px is not None else None
            if latest_px is not None and prev_px:
                change_pct = (latest_px / prev_px - 1) * 100
                c["day_change_pct"] = round(change_pct, 2)
            else:
                c["day_change_pct"] = None

    with (API_DIR / "constituents.json").open("w") as f:
        json.dump(constituents, f, indent=2, ensure_ascii=False)

    print(f"Wrote {API_DIR / 'latest.json'}")
    print(f"Wrote {API_DIR / 'constituents.json'}")
    print(
        f"  Latest: {latest['latest_date']} NAV={latest['latest_nav']} "
        f"(SOXX {latest['benchmarks']['SOXX']['excess_pp']:+.2f}pp, "
        f"QQQ {latest['benchmarks']['QQQ']['excess_pp']:+.2f}pp)"
    )


if __name__ == "__main__":
    main()
