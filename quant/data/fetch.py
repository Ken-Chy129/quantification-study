"""数据获取模块"""

import os
import numpy as np
import pandas as pd


def fetch_stock_daily(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    获取股票日线数据。优先读本地 CSV，没有则尝试 akshare 在线拉取。

    Args:
        symbol: 股票代码，如 "600519"
        start: 起始日期 "YYYYMMDD"
        end: 结束日期 "YYYYMMDD"
    """
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", f"{symbol}.csv"
    )
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, parse_dates=["date"], index_col="date")
        return df.loc[start:end, ["open", "high", "low", "close", "volume"]]

    import akshare as ak

    df = ak.stock_zh_a_hist(
        symbol=symbol, period="daily",
        start_date=start, end_date=end, adjust="qfq",
    )
    df = df.rename(columns={
        "日期": "date", "开盘": "open", "最高": "high",
        "最低": "low", "收盘": "close", "成交量": "volume",
    })
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    return df[["open", "high", "low", "close", "volume"]]


def generate_sample_data(
    start: str = "2022-01-01",
    end: str = "2024-12-31",
    initial_price: float = 1800.0,
    seed: int = 42,
) -> pd.DataFrame:
    """生成模拟股票日线数据，用于网络不可用时测试策略。"""
    np.random.seed(seed)
    dates = pd.bdate_range(start, end)
    n = len(dates)

    daily_returns = np.random.normal(0.0002, 0.018, n)
    close = initial_price * np.cumprod(1 + daily_returns)

    spread = np.random.uniform(0.005, 0.02, n)
    high = close * (1 + spread)
    low = close * (1 - spread)
    open_ = close * (1 + np.random.normal(0, 0.005, n))
    volume = np.random.randint(5000, 50000, n)

    return pd.DataFrame({
        "open": open_, "high": high, "low": low,
        "close": close, "volume": volume,
    }, index=pd.DatetimeIndex(dates, name="date"))
