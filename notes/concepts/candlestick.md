# K线（Candlestick）

## 是什么

用一根"蜡烛"表示一段时间内价格变动的图形，包含开盘价、收盘价、最高价、最低价四个价格。

## 直觉理解

```
    │  ← 上影线（最高价）
  ┌───┐
  │   │  ← 实体（开盘价 ↔ 收盘价）
  └───┘
    │  ← 下影线（最低价）
```

A股红涨绿跌：
- **阳线（红）**：收盘 > 开盘，涨了。实体底=开盘价，顶=收盘价
- **阴线（绿）**：收盘 < 开盘，跌了。反过来

## 代码示例

```python
import akshare as ak
import mplfinance as mpf

df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20260101")
df.index = pd.to_datetime(df['日期'])
df.columns = ['date', 'Open', 'Close', 'High', 'Low', 'Volume', ...]
mpf.plot(df, type='candle', volume=True, title='000001 K线图')
```

## 注意事项

- K线周期可以是任意的：日K、周K、分钟K（1min/5min/15min…）
- **影线含义**：长上影=冲高被打回（上方抛压重），长下影=探底被拉回（下方有支撑），无影线=趋势极强
- K线的 OHLCV 数据是计算所有技术指标（均线、MACD、布林带等）的原材料
- 量化中一般不直接用K线形态（十字星、锤子线），而是把 OHLCV 数值化后提取特征作为因子
