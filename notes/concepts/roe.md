# 净资产收益率 ROE（Return on Equity）

## 是什么

股东每投入 1 块钱，公司能赚回多少。巴菲特最看重的指标。

## 公式

$$ROE = \frac{净利润}{股东权益} \times 100\%$$

杜邦分解：

$$ROE = 净利率 \times 资产周转率 \times 权益乘数$$

## 直觉理解

ROE=20% 意味着股东投入 100 块，公司一年能赚 20 块。长期 ROE>15% 通常是优秀公司的标志。

杜邦分解揭示赚钱的三条路径：
- **高净利率**（茅台模式）：卖得贵
- **高周转率**（沃尔玛模式）：卖得多
- **高杠杆**（银行模式）：借钱赚

## 代码示例

```python
import akshare as ak

# 获取财务指标
df = ak.stock_financial_analysis_indicator(symbol="000001")
# ROE 字段名因数据源而异，常见 roe, roe_diluted
print(df.head())
```

## 注意事项

- ROE 可以被杠杆美化：大量借债（提高权益乘数）会拉高 ROE，需要同时看资产负债率
- 用杜邦分解区分高 ROE 的来源：靠利润率还是靠杠杆，含金量完全不同
- 和 ROA 对比：ROE 高但 ROA 低 → 主要靠杠杆驱动，风险较大
