# 贝塔 (Beta)

## 是什么

衡量策略（或个股）对市场整体波动的**敏感度**。Beta=1 表示跟大盘同涨同跌，Beta>1 放大波动，Beta<1 更稳。

## 公式

$$
\beta = \frac{Cov(R_p, R_m)}{Var(R_m)}
$$

也可以通过对市场收益做线性回归得到斜率：$R_p = \alpha + \beta \cdot R_m + \epsilon$

## 直觉理解

| Beta | 含义 |
|------|------|
| 0 | 和大盘完全无关（如货币基金） |
| 0.5 | 大盘跌 10%，你大约跌 5% |
| 1.0 | 和大盘同步 |
| 1.5 | 大盘涨 10%，你大约涨 15%（但跌也放大） |
| 负值 | 和大盘反着走（少见，某些对冲策略） |

类比：Beta 是你坐的那条船的大小。大船（低 Beta）在风浪中稳，小快艇（高 Beta）颠得厉害但顺风时跑得快。

## 代码示例

```python
import numpy as np

def compute_beta(strategy_returns, market_returns):
    cov = np.cov(strategy_returns, market_returns, ddof=1)[0, 1]
    var_market = np.var(market_returns, ddof=1)
    return cov / var_market
```

## 注意事项

- Beta 不是固定的，会随时间变化——用滚动窗口计算更实际
- 高 Beta 不等于高风险，只是对市场风险敏感；还有很多市场之外的风险 Beta 捕捉不到
- 量化中常说的"市场中性策略"就是把组合 Beta 对冲到接近 0，只留 Alpha
- 和 [Alpha](alpha.md) 是一对概念，回归同一个方程

## 参考

- Investopedia: Beta
- CAPM (Capital Asset Pricing Model)
