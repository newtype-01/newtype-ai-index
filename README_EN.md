# newtype AI Index

[中文](README.md) · **English**

**Ticker: NTAI** · **Inception: 2026-07-17** · **Base value: 100.0000** · **Currency: USD**

A single NAV curve that collapses the seven-layer AI industrial-chain framework from [newtype-equity](https://github.com/newtype-01/newtype-equity) and the judgments of the AI industrial-chain low-frequency signal system into a public record any observer can verify day by day.

This index is not a fund, not investment advice, and does not accept AUM. It exists for one purpose: **to put methodological judgments in a place with verifiable timestamps, so they can be checked after the fact.**

---

## Latest NAV

| Metric | Value |
|---|---|
| Latest trading day | 2026-07-31 |
| NTAI NAV | **96.4920** |
| NTAI period return | **-3.51%** |
| SOXX period return | -3.24% |
| QQQ period return | -1.06% |
| Excess vs SOXX | **-0.27 pp** |
| Excess vs QQQ | **-2.45 pp** |

## NAV Curve

![NAV comparison](charts/nav-comparison.png)

**Opening read**: From 07-17 to 07-23, the index outran both SOXX and QQQ by roughly 8 percentage points, peaking at 109. From 07-24 the AI complex started drawing down, and 07-29 saw a single-day cliff (NVDA -3.6%, MU -10%, VRT -17%, NBIS -12%). In the rebound, QQQ recovered faster thanks to broader diversification; the index recovered in step with SOXX but did not reclaim base value. **First-month NAV lags SOXX by 0.27 pp and QQQ by 2.45 pp.**

This drawdown is not hidden. The index was built as a research record from day one, not as promotional material.

## Current Constituents (Effective 2026-07-17)

| Ticker | Name | Layer | Layer Name | Tier | Weight |
|---|---|---|---|---|---|
| NVDA | NVIDIA | L4 | Compute Hardware | Core | 22% |
| MU | Micron | L3 | Interconnect & Memory | Core | 22% |
| VRT | Vertiv | L2 | Infrastructure | Core | 22% |
| CEG | Constellation Energy | L1 | Energy | N-Stack | 12% |
| TSM | Taiwan Semi | L4 | Compute Hardware | Bridge | 10% |
| MRVL | Marvell | L4 | Compute Hardware | N-Stack | 6% |
| NBIS | Nebius | L5 | Cloud / IaaS | N-Stack | 6% |

- Layer coverage: **L1–L5** (energy through IaaS). L6/L7 excluded for now due to valuation dispersion.
- Tier distribution: Core 66% · N-Stack 24% · Bridge 10%
- Weights sum to **100%** — pure AI exposure, no cash buffer.

Full constituent definitions (including scarcity, shovel-vs-gold, endgame view, etc.) live in [`data/constituents/2026-07-17.json`](data/constituents/2026-07-17.json).

## Time-Asymmetry Disclosure

This repository's first public commit is **on 2026-08-01**, later than the index inception date (2026-07-17). That means the NAV curve from 07-17 to 07-31 is backfilled computation, not a real-time public feed.

To keep the record honest:

- Constituent selection comes entirely from the AI industrial-chain low-frequency signal system's baseline judgment (as_of 2026-07-19). That judgment's git commit timestamp lives in a private repo and can be verified independently.
- Any future constituent change **must be committed before its effective date**. Historical files are never modified (git append-only).
- Old constituents files never change; new adjustments are added as new files.

The index's credibility rests on "publicly verifiable rebalance timestamps." That is what separates it from social-media-style stock picking.

## Repository Layout

```
newtype-ai-index/
├── README.md                       # Chinese (default)
├── README_EN.md                    # English
├── LICENSE                         # MIT
├── docs/
│   └── methodology.md              # Full methodology
├── data/
│   ├── constituents/
│   │   └── 2026-07-17.json         # Constituent definitions on effective date
│   ├── prices/
│   │   └── close_prices.csv        # Daily close for constituents and benchmarks
│   ├── nav/
│   │   ├── daily.csv               # NTAI daily NAV
│   │   └── monthly.csv             # NTAI month-end NAV
│   └── benchmarks/
│       └── comparison.csv          # NTAI vs SOXX vs QQQ (rebased)
├── charts/
│   └── nav-comparison.png          # Comparison chart
└── scripts/
    ├── calculate_nav.py            # NAV computation (stdlib)
    └── generate_chart.py           # Chart generation (matplotlib)
```

## Reproduction

```bash
# Requires Python 3.10+ and matplotlib
python3 scripts/calculate_nav.py
python3 scripts/generate_chart.py
```

Price data lives in `data/prices/close_prices.csv`, sourced from Perplexity Finance. To use your own data provider (Yahoo Finance, Alpha Vantage, etc.), replace this CSV; keep column names as `date,ticker,close`.

## Disclaimer

- **The index is a research tool, not an investment product.** It is not a buy or sell signal and not investment advice.
- **Constituent weights are model targets, not the author's actual holdings.**
- **Past NAV does not predict future performance.**
- **This index is built by an individual retail investor, not a licensed institution.** No AUM, no discretionary management.

## Related Repositories

- [newtype-equity](https://github.com/newtype-01/newtype-equity) — Seven-layer AI industrial-chain analysis framework skill (public)
- AI industrial-chain low-frequency signal system — Low-frequency signal system and monthly reports (private)

## License

MIT · Copyright © 2026 Huang Yihe

---

## Links

- YouTube: [youtube.com/@huanyihe777](https://www.youtube.com/@huanyihe777)
- Twitter: [x.com/huangyihe](https://x.com/huangyihe)
- Substack: [newtype.pro](https://newtype.pro/)
