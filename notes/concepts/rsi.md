# RSI（相对强弱指标，Relative Strength Index）

## 是什么

衡量最近一段时间里，涨的力度占总波动的比例。取值 0~100。

## 公式

$$RSI = \frac{平均上涨幅度}{平均上涨幅度 + 平均下跌幅度} \times 100$$

常用周期：14 天。

## 直觉理解

最近 14 天天天涨 → RSI≈100；天天跌 → RSI≈0。

```
100 ┬───────────────────
    │       超买区
 70 ┤─ ─ ─ ─ ─ ─ ─ ─ ─  ← 超买线
    │     正常波动区
 30 ┤─ ─ ─ ─ ─ ─ ─ ─ ─  ← 超卖线
    │       超卖区
  0 ┴───────────────────
```

| RSI 范围 | 含义 |
|----------|------|
| > 70 | 超买：近期涨太多，可能回调 |
| 30~70 | 正常区间 |
| < 30 | 超卖：近期跌太多，可能反弹 |

## 代码示例

```python
import pandas as pd

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df['rsi'] = calc_rsi(df['close'])
```

## 注意事项

- RSI 是**滞后指标**，描述已经发生的涨跌，不是预测
- **"超买就卖"是新手陷阱**：强势股可以 RSI>70 持续数周甚至数月，超买 ≠ 要跌
- 均线多头排列 + RSI 50~70 = 趋势向上且力度健康
- RSI 背离（价格新高但 RSI 未新高）比单纯超买超卖更有参考价值
