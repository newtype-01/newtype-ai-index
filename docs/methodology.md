# newtype AI Index 方法论

## 一、定位

**newtype AI Index(代号 NTAI)** 是一个模型追踪指数,用来把 [newtype-equity](https://github.com/newtype-01/newtype-equity) 的七层 AI 产业链分析框架与 [ai-signal-system](https://github.com/newtype-01/ai-signal-system) 的低频信号,收敛成一条可以每日观察的净值曲线。

Index 不是投资产品,不是基金,不是"跟车"标的。它服务的目的只有一个:**把方法论的判断结果放到公开、时间戳可查的地方**,让任何人可以在事后对照曲线判断这套框架是不是空谈。

## 二、Index 与 Baseline 的关系

Index 的成分来自 [ai-signal-system 的 baseline 报告(2026-07-19)](https://github.com/newtype-01/ai-signal-system/blob/main/reports/baseline-2026-07-19.md)和其 [universe.json](https://github.com/newtype-01/ai-signal-system/blob/main/config/universe.json) 分类。Universe 划出 Core / N-Stack / Watch / Skip 四档,Index 只在 Core 与 N-Stack 中选,并把一档特殊的 Bridge 位置(TSM)显式标注理由。

Universe 是"能不能进池子",Index 是"进了池子怎么配"。两者是父子关系,不是同一件事。

## 三、时间不对称的诚实标注

**本仓库的初始 commit 时间戳晚于 Index 的起始日(2026-07-17)**。

- Index 起始日 **2026-07-17**(2026-07-19 是周日,取最近的前一交易日作为净值基准日)
- Baseline 报告的 as_of 日期 **2026-07-19** — 这个报告的 git commit 时间戳在 [ai-signal-system 仓库](https://github.com/newtype-01/ai-signal-system) 里,可以独立验证
- 本仓库首次公开 commit **2026-08-01**

也就是说,**Index 的成分选择并非在 07-17 那天公开锁定的**。它是对 baseline 那一期私有判断的公开追认,不是事后编造。为避免误解:

1. 所有 07-17 到 08-01 的净值,是**回填计算**,不是实时公开发布
2. 未来任何成分调整,必须在生效日之前 commit 到本仓库,不允许改历史文件
3. baseline 报告的 git 时间戳提供第一道独立时间证明

## 四、成分选择规则

### 4.1 池子

只从 baseline universe 的 **Core** 和 **N-Stack** 里选。**Watch** 只作为特殊情况(见下)。**Skip** 永不入选。

### 4.2 权重档位

- **Core 重仓**:22%
- **Core 标配**:12%
- **N-Stack 试仓**:6%
- **Bridge 特殊位**:10%

单只上限 25%,单层上限 50%,现金比例 0%(纯 AI 敞口,不留缓冲)。

### 4.3 层级覆盖

必须覆盖 seven-layer 中的 **L1(能源)、L2(基建)、L3(内存互联)、L4(算力硬件)、L5(云 IaaS)** 五层。L6/L7(平台与应用)因为估值离散度过大,当前 Index 不纳入。这是"应用层悖论"课程里讨论过的判断的直接体现。

### 4.4 Bridge 特殊说明

**TSM** 在 baseline universe 里被标为 Watch 层(0-8% 权重区间),但 Index 显式给了 10% 权重并标为 Bridge。理由是 TSM 是 AI 算力的物理制造基础,不放入会让 L4 层过度集中在 fabless。这是 Index 相对 universe 的**唯一一处主动加仓**,需要单独辩护。

## 五、净值计算

### 5.1 基准日与初始净值

- 基准日:**2026-07-17**(收盘)
- 初始净值:**100.0000**
- 计价货币:**USD**

### 5.2 收益率算法

**目标权重跟踪(target-weight tracking),每月首个交易日再平衡**。

具体:

- 基准日按目标权重把 100 元名义净值分配到各成分,记录各自"份额数"(name shares)
- 每月首个交易日,把当日投资组合估值分子分母重算,再按目标权重重新分配份额数
- 月内保持份额数不变,每日按当日收盘价重估净值

这个规则会**主动抑制 buy-and-hold drift**。想反映的是"如果一个投资者严格按目标权重跟踪这套框架会得到什么结果",不是"如果只在基准日买一次然后放着不动会怎样"。

### 5.3 无股息、无成本假设

- **不计入股息** — 都是低股息或不派息的成长股,月度尺度可忽略
- **不计入交易成本** — Index 是模型追踪,不是实盘;真实交易的滑点、税负、佣金由使用者自己承担
- **不做汇率调整** — 只跟踪美股 USD 计价的价格

### 5.4 数据来源

日收盘价来自 **Perplexity Finance**(见 `data/prices/close_prices.csv`)。数据出现异常时,以 Perplexity Finance 后续更新为准,并在 changelog 中记录调整。

## 六、调仓规则

**Index 的生死线:任何调仓必须在生效日之前 commit 到本仓库。**

### 6.1 触发场景

1. **月度再平衡**:每月首个交易日,按当前 constituents 文件的目标权重重新分配份额。这不算调仓,只是权重复位。
2. **成分调整**:换股、加仓、减仓、调权重,都必须:
   - 在 `data/constituents/` 目录下新增一个文件,文件名为生效日 `YYYY-MM-DD.json`
   - Commit 时间必须早于文件名对应的日期
   - 老文件不得改动(git append-only)
3. **公司事件**:退市、被收购、分拆,按公告日或除牌日作为强制成分调整触发。

### 6.2 频率上限

原则上一个自然月最多一次成分调整。频繁调仓会破坏 Index 作为"低频信号"的定位。特殊事件除外。

### 6.3 Universe 变更传导

Universe 是父,Index 是子。Universe 每季度重审一次(在 ai-signal-system 仓库),Index 在下一个季度首月的月度再平衡日按新 universe 复核成分。

## 七、免责边界

- **Index 是研究工具,不是投资产品**。不构成买入或卖出信号,不构成投资建议。
- **成分权重是模型目标,不是本人实际持仓**。本人的实际投资仓位与 Index 不必然一致。
- **过往净值不代表未来表现**。回填期(07-17 到 08-01)的曲线只是把方法论的判断放到坐标上,不能证明这套框架未来仍会有效。
- **本 Index 的构建方是散户个人,不是持牌机构**。不接受 AUM,不接受管理费,不代客理财。

## 八、跟哪些标的可以对照

Index 用两个基准做对比:

- **SOXX**(iShares Semiconductor ETF)— 半导体行业 ETF,是 Index 的近似同板块基准
- **QQQ**(Invesco QQQ Trust)— 纳斯达克 100 ETF,是 Index 的宽基科技对照

**跑赢 SOXX** 才有意义 — 说明"七层框架 + 主动权重"相对被动持有整个半导体 ETF 有超额。**跑赢 QQQ** 只是次要参考 — 集中持股跑赢宽基是应该的,跑输才需要解释。

## 九、变更历史

见根目录 `CHANGELOG.md`。所有影响净值计算或成分定义的变更都会记录。
