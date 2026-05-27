"""双均线交叉策略

规则：
- 短期均线上穿长期均线 → 买入（金叉）
- 短期均线下穿长期均线 → 卖出（死叉）
- 全仓进出，不加杠杆
"""

import pandas as pd
import numpy as np


def sma_cross_signals(
    close: pd.Series,
    short_window: int = 5,
    long_window: int = 20,
) -> pd.DataFrame:
    """
    生成双均线交叉信号。

    Returns:
        DataFrame with columns:
        - sma_short: 短期均线
        - sma_long: 长期均线
        - signal: 1=持仓, 0=空仓
        - trade: 1=买入, -1=卖出, 0=无操作
    """
    df = pd.DataFrame({"close": close})
    df["sma_short"] = close.rolling(short_window).mean()
    df["sma_long"] = close.rolling(long_window).mean()

    # 短均线 > 长均线 → 持仓
    df["signal"] = np.where(df["sma_short"] > df["sma_long"], 1, 0)

    # trade: signal 变化的那一天
    df["trade"] = df["signal"].diff()

    return df


def backtest(
    df: pd.DataFrame,
    signals: pd.DataFrame,
    commission: float = 0.001,
) -> pd.DataFrame:
    """
    基于信号做简单回测。

    Args:
        df: 原始行情数据（需含 close 列）
        signals: sma_cross_signals 的输出
        commission: 单边手续费率（默认万分之十 = 0.1%）

    Returns:
        DataFrame with columns:
        - daily_return: 策略日收益率
        - cumulative_return: 策略累计收益
        - benchmark_return: 基准（买入持有）累计收益
    """
    result = pd.DataFrame(index=df.index)

    # 持仓收益：今天的收益 = 昨天的仓位 × 今天的涨跌幅
    market_return = df["close"].pct_change()
    result["daily_return"] = signals["signal"].shift(1) * market_return

    # 扣除手续费：交易日扣两次（买+卖各一次手续费）
    trade_cost = signals["trade"].abs() * commission
    result["daily_return"] -= trade_cost

    result["cumulative_return"] = (1 + result["daily_return"]).cumprod()
    result["benchmark_return"] = (1 + market_return).cumprod()

    return result


def calc_metrics(result: pd.DataFrame) -> dict:
    """计算策略绩效指标"""
    returns = result["daily_return"].dropna()
    cum = result["cumulative_return"].dropna()

    total_return = cum.iloc[-1] / cum.iloc[0] - 1
    days = len(returns)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 0 else 0

    # 夏普比率
    sharpe = (
        np.mean(returns) / np.std(returns, ddof=1) * np.sqrt(252)
        if np.std(returns, ddof=1) > 0
        else 0
    )

    # 最大回撤
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    max_drawdown = drawdown.min()

    # 交易次数
    trades = result.get("daily_return", returns)
    benchmark_return = result["benchmark_return"].dropna()
    bench_total = benchmark_return.iloc[-1] / benchmark_return.iloc[0] - 1

    return {
        "total_return": f"{total_return:.2%}",
        "annual_return": f"{annual_return:.2%}",
        "benchmark_total": f"{bench_total:.2%}",
        "sharpe_ratio": f"{sharpe:.2f}",
        "max_drawdown": f"{max_drawdown:.2%}",
        "trading_days": days,
    }
