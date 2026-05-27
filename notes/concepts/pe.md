# 市盈率 PE（Price-to-Earnings Ratio）

## 是什么

股价除以每股收益，衡量你为公司每赚 1 块钱愿意付多少钱。

## 公式

$$PE = \frac{股价}{每股收益(EPS)}$$

## 直觉理解

PE=20 意味着按当前利润需要 20 年回本。越低越"便宜"，但必须同行业比较才有意义——银行 PE 普遍 5~8，科技股 30~50 是常态。

## 代码示例

```python
import akshare as ak

# 获取个股估值指标
df = ak.stock_a_indicator_lg(symbol="000001")
print(df[['trade_date', 'pe', 'pe_ttm']].tail())
```

## 注意事项

- 亏损公司 PE 为负，没有意义
- 周期股（钢铁、养殖）PE 最低时往往是盈利顶峰，反而该卖出
- 量化中常用 **1/PE（EP，盈利收益率）** 代替，避免负值和极端值问题
- 区分静态 PE（用上年利润）和滚动 PE_TTM（用最近四个季度利润），TTM 更及时
