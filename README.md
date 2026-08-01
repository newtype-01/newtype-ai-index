# newtype AI Index

**代号:NTAI** · **起始日:2026-07-17** · **初始净值:100.0000** · **计价货币:USD**

用一条净值曲线,把 [newtype-equity](https://github.com/newtype-01/newtype-equity) 的七层 AI 产业链框架和 [ai-signal-system](https://github.com/newtype-01/ai-signal-system) 的低频信号,收敛成任何人可以每日检验的公开记录。

Index 不是基金,不是投资建议,不接受 AUM。它只做一件事:**把方法论的判断放在时间戳可查的地方,让事后有据可对**。

---

## 最新净值

| 指标 | 值 |
|---|---|
| 最新交易日 | 2026-07-31 |
| NTAI 净值 | **96.4920** |
| NTAI 期间收益 | **-3.51%** |
| SOXX 期间收益 | -3.24% |
| QQQ 期间收益 | -1.06% |
| 相对 SOXX 超额 | **-0.27 pp** |
| 相对 QQQ 超额 | **-2.45 pp** |

## 净值曲线

![NAV comparison](charts/nav-comparison.png)

**开局解读**:07-17 到 07-23,Index 前期把 SOXX 和 QQQ 都甩开约 8 个百分点,峰值 109。07-24 起 AI 板块整体回撤,07-29 出现单日跳崖(NVDA 单日 -3.6%,MU -10%,VRT -17%,NBIS -12%)。反弹阶段 QQQ 因分散度更高恢复更快,Index 与 SOXX 同步反弹但未回到基准。**首月净值跑输 SOXX 0.27 pp、跑输 QQQ 2.45 pp**。

这段回撤没有被藏起来。事实上,Index 从建立起就是研究记录用的,而不是宣传素材。

## 当前成分(生效日 2026-07-17)

| Ticker | 名称 | 层 | 层名 | Tier | 权重 |
|---|---|---|---|---|---|
| NVDA | NVIDIA | L4 | Compute Hardware | Core | 22% |
| MU | Micron | L3 | Interconnect & Memory | Core | 22% |
| VRT | Vertiv | L2 | Infrastructure | Core | 22% |
| CEG | Constellation Energy | L1 | Energy | N-Stack | 12% |
| TSM | Taiwan Semi | L4 | Compute Hardware | Bridge | 10% |
| MRVL | Marvell | L4 | Compute Hardware | N-Stack | 6% |
| NBIS | Nebius | L5 | Cloud / IaaS | N-Stack | 6% |

- 层覆盖:**L1-L5**(能源到 IaaS),L6/L7 因估值离散度过大暂不纳入
- Tier 分布:Core 66% · N-Stack 24% · Bridge 10%
- 权重合计:**100%**(纯 AI 敞口,无现金缓冲)

完整成分定义(含 scarcity、shovel-vs-gold、endgame view 等属性)见 [`data/constituents/2026-07-17.json`](data/constituents/2026-07-17.json)。

## 时间不对称的诚实标注

本仓库首次公开 commit **在 2026-08-01**,晚于 Index 起始日(2026-07-17)。也就是 07-17 到 07-31 的净值曲线,是回填计算,不是当时实时发布的记录。

为避免混淆:

- 成分选择完全来自 [ai-signal-system 的 baseline 报告(2026-07-19)](https://github.com/newtype-01/ai-signal-system/blob/main/reports/baseline-2026-07-19.md),那份报告的 git commit 时间戳可以独立验证
- 未来任何成分调整,**必须在生效日之前 commit** 到本仓库,不允许事后改历史文件(git append-only)
- 老 constituents 文件永远不动,新调整只加新文件

Index 的可信度来自"公开可验证的调仓时间戳",这是它跟社交媒体口播式喊单的核心区别。

## 仓库结构

```
newtype-ai-index/
├── README.md                       # 本文件
├── LICENSE                         # MIT
├── docs/
│   └── methodology.md              # 方法论全文
├── data/
│   ├── constituents/
│   │   └── 2026-07-17.json         # 生效日的完整成分定义
│   ├── prices/
│   │   └── close_prices.csv        # 成分和基准的日收盘价
│   ├── nav/
│   │   ├── daily.csv               # NTAI 日净值
│   │   └── monthly.csv             # NTAI 月末净值
│   └── benchmarks/
│       └── comparison.csv          # NTAI vs SOXX vs QQQ(rebased)
├── charts/
│   └── nav-comparison.png          # 对比曲线
└── scripts/
    ├── calculate_nav.py            # 净值计算(标准库)
    └── generate_chart.py           # 曲线生成(matplotlib)
```

## 复现方法

```bash
# 需要 Python 3.10+ 和 matplotlib
python3 scripts/calculate_nav.py
python3 scripts/generate_chart.py
```

价格数据在 `data/prices/close_prices.csv`,来自 Perplexity Finance。如果想用你自己的数据源(Yahoo Finance、Alpha Vantage 等),替换这个 CSV,列名保持 `date,ticker,close` 即可。

## 免责

- **Index 是研究工具,不是投资产品**。不构成买入或卖出信号,不构成投资建议
- **成分权重是模型目标,不是本人实际持仓**
- **过往净值不代表未来表现**
- **本 Index 的构建方是散户个人,不是持牌机构**。不接受 AUM,不代客理财

## 相关仓库

- [newtype-equity](https://github.com/newtype-01/newtype-equity) — 七层 AI 产业链分析框架 skill(公开)
- ai-signal-system — 低频信号系统与月度报告(私有)

## 许可

MIT · Copyright © 2026 Huang Yihe
