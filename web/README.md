# Web 嵌入组件

三个文件,渐进式:先看 `page.html`,复制到你的静态 HTML 站作为 Index 子页面即可。

## 文件清单

| 文件 | 用途 |
|---|---|
| **`page.html`** | **完整子页面**:上半走势图 + 下半公司卡片,单文件独立运行。newtype.pro 的 Index 子页面直接用这个。 |
| `embed.html` | 只要走势图组件的独立示例 |
| `cards.html` | 只要公司卡片组件的独立示例 |

## 数据源

两个组件消费两个 JSON,都由 GitHub Actions 每交易日自动更新:

- **走势图**:`https://raw.githubusercontent.com/newtype-01/newtype-ai-index/main/data/api/latest.json`
  - 含起始到最新的完整时间序列,以及 NTAI/SOXX/QQQ 的期间收益汇总
- **公司卡片**:`https://raw.githubusercontent.com/newtype-01/newtype-ai-index/main/data/api/constituents.json`
  - 含每只成分的 layer/tier/scarcity/role/watch_reason,以及**每日更新的最新收盘价和日涨跌幅**

## 嵌入 newtype.pro 的两种方式

### 方式 A(推荐):直接用 page.html

复制 `page.html` 的全部内容作为你 Index 子页面的 body,或者拆出 `<style>` 到你的全局 CSS、`<script>` 到独立 JS 文件。

Chart.js 从 CDN 引入,不需要打包。

### 方式 B:只嵌走势图或只嵌卡片

分别复制 `embed.html` 或 `cards.html` 里的 style + 容器 div + script 部分。

## 缓存策略建议

- raw.githubusercontent.com 默认 CDN 缓存约 5 分钟
- 建议在你的静态站或 CDN 层再套一层缓存(15 分钟以内),数据更新频率是每交易日一次,过高的刷新是浪费

## CSS 变量适配

组件用了硬编码的暗色配色。如果你 newtype.pro 有主色系统,需要调整这几个 hex 值:

- `#e6b800` — NTAI 主色(黄)
- `#4aa3df` — SOXX(蓝)
- `#8e8e93` — QQQ(灰)
- `#4caf50` / `#e57373` — 涨/跌颜色
- `#0e1116` / `#14181f` / `#1c2129` — 三层背景
- `#22262d` / `#2a2f38` — 边框
- `#f0f2f5` / `#e0e2e6` / `#c5c8cc` / `#a0a4ab` / `#6b6f76` — 五级文字

## 数据字段参考

**latest.json**:
```json
{
  "index_name": "newtype AI Index",
  "index_ticker": "NTAI",
  "inception_date": "2026-07-17",
  "base_nav": 100.0,
  "latest_date": "2026-07-31",
  "latest_nav": 96.4920,
  "period_return_pct": -3.51,
  "benchmarks": {
    "SOXX": { "latest": 96.76, "period_return_pct": -3.24, "excess_pp": -0.27 },
    "QQQ":  { "latest": 98.94, "period_return_pct": -1.06, "excess_pp": -2.45 }
  },
  "series": [ { "date": "2026-07-17", "ntai": 100.0, "soxx": 100.0, "qqq": 100.0 } ],
  "updated_at_utc": "2026-08-02T21:35:00Z"
}
```

**constituents.json**:
```json
{
  "meta": { "effective_date": "2026-07-17", ... },
  "price_snapshot": { "latest_date": "2026-07-31", "prev_date": "2026-07-30" },
  "constituents": [
    {
      "ticker": "NVDA",
      "name": "NVIDIA Corporation",
      "primary_layer": 4,
      "layer_name": "Compute Hardware",
      "tier": "Core",
      "weight": 0.22,
      "scarcity": "core_scarcity",
      "shovel_vs_gold": "shovel",
      "endgame_view": "endgame_candidate",
      "role": "GPU算力硬件核心,定义加速计算与互联架构",
      "watch_reason": "数据中心收入、毛利率、下一季度指引是算力层最直接温度计",
      "stack_layers": [4, 3, 5],
      "latest_price": 200.75,
      "day_change_pct": 2.93
    }
  ]
}
```
