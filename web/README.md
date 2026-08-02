# Web 嵌入组件

这个目录提供一段可以直接嵌入任意静态 HTML 页面的走势图组件,消费的是 [`data/api/latest.json`](../data/api/latest.json)。

## 文件

- **`embed.html`** — 完整的独立示例,包含 CSS、HTML 容器、Chart.js 调用。可以直接用浏览器打开预览,也可以按需拆分嵌入到你自己的页面。

## 数据源

前端只需要 fetch 一个 URL:

```
https://raw.githubusercontent.com/newtype-01/newtype-ai-index/main/data/api/latest.json
```

这个 JSON 由 GitHub Actions 每个交易日自动更新。返回结构:

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
  "series": [ { "date": "2026-07-17", "ntai": 100.0, "soxx": 100.0, "qqq": 100.0 }, ... ],
  "updated_at_utc": "2026-08-01T21:35:00Z",
  "source": "https://github.com/newtype-01/newtype-ai-index"
}
```

## 嵌入 newtype.pro 的三步

1. **在目标 HTML 页面 `<head>` 加 Chart.js CDN**:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
   ```

2. **在页面 body 里放一个容器 div**:
   ```html
   <div id="ntai-widget" class="ntai-widget"></div>
   ```

3. **把 `embed.html` 里的 `<style>` 和 `<script>` 部分复制到你的页面**(或者拆出 `ntai-widget.css` / `ntai-widget.js` 独立托管)。

## 缓存策略建议

- raw.githubusercontent.com 默认 CDN 缓存约 5 分钟
- 如果你的网站有反向代理,可以再套一层缓存(比如 Cloudflare Cache Rules 缓存 15 分钟)
- 数据更新频率是每交易日一次,过高的缓存刷新是浪费

## 未来扩展方向

- **公司卡片组件**:消费 `data/api/constituents.json`,展示每只成分的 layer/tier/rationale/最新价格。占位,下一步做。
- **月度净值弹窗**:点击图上任意日期,弹出该月月末净值 vs SOXX/QQQ 的详细对比表。
- **CSV 下载按钮**:直接指向 `data/nav/daily.csv` 或 `data/benchmarks/comparison.csv` 的 raw URL。

有 iframe 需求也可以做,但建议优先直嵌——CSS 变量可以跟你 newtype.pro 的主色适配。
