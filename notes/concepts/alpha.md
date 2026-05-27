# 阿尔法 (Alpha)

## 是什么

策略收益中**不能被市场整体涨跌解释**的那部分超额收益。Alpha 高说明策略本身有"真本事"，而不是简单跟着大盘赚钱。

## 公式

$$
\alpha = R_p - [R_f + \beta \times (R_m - R_f)]
$$

- $R_p$：策略收益率
- $R_f$：无风险利率
- $R_m$：市场基准收益率（如沪深 300）
- $\beta$：策略对市场的敏感度（见 [Beta](beta.md)）

方括号内是"市场本身就能给你的收益"，减掉它剩下的就是你的真功夫。

## 直觉理解

大盘涨了 10%，你的策略涨了 15%。如果你的 β=1（跟大盘同步），那 Alpha ≈ 5%——这 5% 是你选股/择时带来的。

反过来，大盘涨 10% 你赚 8%、β=1，Alpha 是负的——还不如买指数基金。

类比：班里考试平均分 80，你考了 90。Alpha 就是你超出平均水平的那 10 分，代表你自己的实力而非试卷简单。

## 代码示例

```python
import numpy as np
from scipy import stats

def compute_alpha(strategy_returns, market_returns, risk_free_rate=0.0):
    excess_strategy = strategy_returns - risk_free_rate / 252
    excess_market = market_returns - risk_free_rate / 252
    beta, alpha_daily, _, _, _ = stats.linregress(excess_market, excess_strategy)
    alpha_annual = alpha_daily * 252
    return alpha_annual, beta
```

## 注意事项

- Alpha 高度依赖你选的基准——换一个基准，Alpha 可能完全不同
- 回测里的 Alpha 可能是过拟合的产物，样本外才算数
- Alpha 和 Beta 是一对，单看 Alpha 不看 Beta 没意义
- 量化行业常说的"挖 Alpha"就是找能持续产生超额收益的因子或策略

## 参考

- Investopedia: Jensen's Alpha
- 《主动投资组合管理》(Active Portfolio Management)
