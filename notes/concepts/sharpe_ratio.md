# 夏普比率 (Sharpe Ratio)

## 是什么

衡量每承受一单位风险能获得多少超额收益。越高越好，但要看上下文。

## 公式

$$
Sharpe = \frac{R_p - R_f}{\sigma_p}
$$

- $R_p$：策略年化收益率
- $R_f$：无风险利率（通常取国债收益率，简化时用 0）
- $\sigma_p$：策略收益的年化标准差

日频数据年化：$Sharpe = \frac{\overline{r_{daily}}}{\sigma_{daily}} \times \sqrt{252}$

## 直觉理解

两个策略都赚 20%，一个波动 10%，一个波动 40%——夏普比率告诉你第一个"性价比"更高。

类比：同样的月薪，一个每月稳定到账，一个有时发两倍有时不发——你更愿意要哪个？

## 经验值

| 夏普 | 含义 |
|------|------|
| < 0 | 亏钱 |
| 0 - 1 | 一般 |
| 1 - 2 | 不错 |
| > 2 | 非常好（警惕过拟合） |

## 代码示例

```python
import numpy as np

def sharpe_ratio(daily_returns, risk_free_rate=0.0):
    excess = daily_returns - risk_free_rate / 252
    return np.mean(excess) / np.std(excess, ddof=1) * np.sqrt(252)
```

## 注意事项

- 夏普高不代表策略好：可能只是回测周期恰好在牛市
- 夏普对极端亏损不敏感（因为用标准差，上下波动等权）——补充看最大回撤和卡玛比率
- 不同数据频率算出的夏普不直接可比

## 参考

- Investopedia: Sharpe Ratio
