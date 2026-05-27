# 总资产收益率 ROA（Return on Assets）

## 是什么

公司每 1 块钱总资产能产生多少利润，反映整体资产使用效率。

## 公式

$$ROA = \frac{净利润}{总资产} \times 100\%$$

## 直觉理解

ROA 和 ROE 的区别：ROE 只看股东自己投的钱赚了多少，ROA 把借来的钱也算进去。

一个公司股东投了 100 块，又借了 900 块，总资产 1000 块，赚了 50 块：
- ROE = 50/100 = 50%（看着很猛）
- ROA = 50/1000 = 5%（其实资产效率一般）

ROA 更能反映公司真实的运营能力，不受杠杆"美颜"影响。

## 代码示例

```python
import akshare as ak

df = ak.stock_financial_analysis_indicator(symbol="000001")
print(df.head())
```

## 注意事项

- ROA 跨行业比较意义不大（银行天然低 ROA 高杠杆，科技公司天然高 ROA 低杠杆）
- ROE 高 + ROA 低 = 杠杆驱动型，风险较高
- ROE 高 + ROA 也高 = 真正的好公司，靠经营能力赚钱
