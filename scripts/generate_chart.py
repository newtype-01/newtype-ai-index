#!/usr/bin/env python3
"""Generate NAV comparison chart: NTAI vs SOXX vs QQQ.

Reads data/benchmarks/comparison.csv, writes charts/nav-comparison.png.
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator

ROOT = Path(__file__).resolve().parent.parent
COMPARISON = ROOT / "data" / "benchmarks" / "comparison.csv"
OUT = ROOT / "charts" / "nav-comparison.png"


def main() -> None:
    dates = []
    ntai = []
    soxx = []
    qqq = []
    with COMPARISON.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(datetime.strptime(row["date"], "%Y-%m-%d").date())
            ntai.append(float(row["ntai"]))
            soxx.append(float(row["soxx"]))
            qqq.append(float(row["qqq"]))

    fig, ax = plt.subplots(figsize=(11, 6), dpi=140)
    fig.patch.set_facecolor("#0e1116")
    ax.set_facecolor("#0e1116")

    ax.plot(dates, ntai, color="#e6b800", linewidth=2.4, label="newtype AI Index (NTAI)", zorder=5)
    ax.plot(dates, soxx, color="#4aa3df", linewidth=1.6, label="SOXX (iShares Semiconductor ETF)", zorder=4)
    ax.plot(dates, qqq, color="#8e8e93", linewidth=1.6, label="QQQ (Invesco QQQ Trust)", zorder=3)

    # Baseline
    ax.axhline(100, color="#3a3f47", linewidth=0.8, linestyle="--", zorder=1)

    # Grid & spines
    ax.grid(True, color="#22262d", linewidth=0.6, zorder=0)
    for s in ax.spines.values():
        s.set_color("#3a3f47")
    ax.tick_params(colors="#a0a4ab", labelsize=9)

    ax.set_title(
        "newtype AI Index vs Benchmarks (rebased to 100 on 2026-07-17)",
        color="#f0f2f5",
        fontsize=13,
        pad=12,
        loc="left",
    )
    ax.set_ylabel("NAV (rebased)", color="#a0a4ab", fontsize=10)

    ax.xaxis.set_major_locator(DayLocator(interval=2))
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    fig.autofmt_xdate(rotation=0, ha="center")

    # End-of-series labels
    last_d = dates[-1]
    for name, val, color in [
        ("NTAI", ntai[-1], "#e6b800"),
        ("SOXX", soxx[-1], "#4aa3df"),
        ("QQQ", qqq[-1], "#8e8e93"),
    ]:
        ax.annotate(
            f"{name} {val:.2f}",
            xy=(last_d, val),
            xytext=(6, 0),
            textcoords="offset points",
            color=color,
            fontsize=9,
            fontweight="bold",
            va="center",
        )

    legend = ax.legend(
        loc="lower left",
        frameon=False,
        labelcolor="#e0e2e6",
        fontsize=9,
    )

    # Footer note
    fig.text(
        0.99,
        0.01,
        "Source: Perplexity Finance close prices. Research-only. Not investment advice.",
        color="#6b6f76",
        fontsize=7.5,
        ha="right",
    )

    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, facecolor=fig.get_facecolor(), bbox_inches="tight")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
