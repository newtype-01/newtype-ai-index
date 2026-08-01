# Changelog

Index 生死线:任何影响净值计算或成分定义的变更都在这里留痕。

## 2026-08-01 — Initial public commit

- 建立 newtype AI Index(代号 NTAI),起始日 2026-07-17,初始净值 100.0000
- 首份成分定义 [`data/constituents/2026-07-17.json`](data/constituents/2026-07-17.json),7 只成分
- 数据来源:[Perplexity Finance](https://www.perplexity.ai/finance) 日收盘价
- 回填期净值:2026-07-17 至 2026-07-31(共 11 个交易日),截止净值 96.4920
- 基准对比:SOXX、QQQ,同基准日 rebase 到 100

**诚实标注**:07-17 到 07-31 的净值是回填计算,不是实时发布。成分选择依据 [ai-signal-system baseline 报告(2026-07-19)](https://github.com/newtype-01/ai-signal-system/blob/main/reports/baseline-2026-07-19.md),其 git commit 时间戳独立可查。此后任何调整都在生效日前 commit。
