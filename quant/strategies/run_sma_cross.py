"""运行双均线交叉策略的入口脚本"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from quant.data.fetch import fetch_stock_daily, generate_sample_data
from quant.strategies.sma_cross import sma_cross_signals, backtest, calc_metrics


def main():
    # --- 参数 ---
    symbol = "600519"       # 贵州茅台
    start = "20220101"
    end = "20241231"
    short_window = 5        # 5 日均线
    long_window = 20        # 20 日均线

    # --- 获取数据 ---
    try:
        print(f"拉取 {symbol} 数据 ({start} ~ {end}) ...")
        df = fetch_stock_daily(symbol, start, end)
    except Exception as e:
        print(f"在线数据获取失败 ({e.__class__.__name__}), 使用模拟数据")
        df = generate_sample_data(start="2022-01-01", end="2024-12-31")
        symbol = "SIMULATED"
    print(f"共 {len(df)} 个交易日")

    # --- 生成信号 ---
    signals = sma_cross_signals(df["close"], short_window, long_window)

    # --- 回测 ---
    result = backtest(df, signals)

    # --- 绩效 ---
    metrics = calc_metrics(result)
    print("\n=== 策略绩效 ===")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # --- 画图 ---
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True,
                              gridspec_kw={"height_ratios": [2, 1]})

    # 上图：价格 + 均线 + 买卖点
    ax1 = axes[0]
    ax1.plot(df.index, df["close"], label="Close", color="#333", linewidth=0.8)
    ax1.plot(signals.index, signals["sma_short"],
             label=f"SMA{short_window}", color="#e74c3c", linewidth=0.8)
    ax1.plot(signals.index, signals["sma_long"],
             label=f"SMA{long_window}", color="#3498db", linewidth=0.8)

    buys = signals[signals["trade"] == 1]
    sells = signals[signals["trade"] == -1]
    ax1.scatter(buys.index, df.loc[buys.index, "close"],
                marker="^", color="#2ecc71", s=60, zorder=5, label="Buy")
    ax1.scatter(sells.index, df.loc[sells.index, "close"],
                marker="v", color="#e74c3c", s=60, zorder=5, label="Sell")

    ax1.set_title(f"{symbol} SMA Cross ({short_window}/{long_window})", fontsize=13)
    ax1.legend(loc="upper left", fontsize=9)
    ax1.set_ylabel("Price")
    ax1.grid(True, alpha=0.3)

    # 下图：累计收益对比
    ax2 = axes[1]
    ax2.plot(result.index, result["cumulative_return"],
             label="Strategy", color="#2ecc71", linewidth=1.2)
    ax2.plot(result.index, result["benchmark_return"],
             label="Buy & Hold", color="#95a5a6", linewidth=1.2)
    ax2.axhline(y=1, color="#bbb", linewidth=0.5, linestyle="--")
    ax2.set_ylabel("Cumulative Return")
    ax2.legend(loc="upper left", fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    plt.tight_layout()
    output_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "results", "sma_cross_result.png"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150)
    print(f"\n图表已保存: {output_path}")


if __name__ == "__main__":
    main()
