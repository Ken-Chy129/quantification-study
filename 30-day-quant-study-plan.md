# 30 天量化交易学习计划

> **目标：** 跑通量化交易最小闭环：数据获取 → 指标计算 → 策略实现 → 回测评估 → 风控 → 报告。30 天后具备独立研究和扩展的能力。
>
> **节奏：** 工作日 30-45 分钟（做一件事），周末 2-3 小时集中产出。
>
> **工程原则：** 从 Day 1 起代码直接写进 `quant/` 模块，notebook 只用于探索验证。

---

## 项目结构（Day 1 初始化）

```
quantification-study/
├── quant/                  # 核心代码模块
│   ├── data/               # 数据加载、清洗
│   ├── indicators/         # 技术指标
│   ├── strategies/         # 策略实现
│   ├── backtest/           # 回测引擎
│   ├── risk/               # 风控模块
│   └── report/             # 报告生成
├── configs/                # 策略参数 YAML
├── notebooks/              # 探索性 notebook
├── notes/                  # 学习笔记
│   ├── daily/              # 较长的单日笔记
│   └── concepts/           # 概念卡片（按主题）
├── docs/                   # 周报、策略报告
├── data/                   # 原始和处理后数据
│   ├── raw/
│   └── processed/
├── results/                # 回测结果
└── PROGRESS.md             # 每日进度追踪
```

---

## 弹性规则

- **落后 1-2 天：** 周末补，优先代码产出，笔记简写
- **落后 3 天以上：** 砍内容不赶进度，跳过复盘日直接进下一周核心任务
- **概念卡住：** 先用代码跑一遍看结果，再回头补理解
- **周复盘不可跳过：** 哪怕只有 5 句话

---

## 4 周路线总览

| 周次 | 主题 | 最低交付物 |
|------|------|-----------|
| 第 1 周 | 基础 + 数据 + 指标 | `quant/data/` + `quant/indicators/` 可用 |
| 第 2 周 | 回测引擎 + 第一个策略 | `quant/backtest/` + 双均线策略可运行 |
| 第 3 周 | 更多策略 + 风控 | 3 个策略 + `quant/risk/` 风控模块 |
| 第 4 周 | 报告 + 整合 + 复盘 | 完整回测报告，明确下一步方向 |

---

## 第 1 周：基础 + 数据 + 指标

> 目标：能拉数据、算指标、画图。这周结束后 `quant/data/` 和 `quant/indicators/` 可用。

- [ ] **Day 1 | 全景 + 初始化** — 初始化 repo 目录结构；理解量化链路：数据 → 策略 → 回测 → 风控 → 执行 → 复盘
- [ ] **Day 2 | 数据获取** — 用 yfinance 拉 SPY 数据，保存到 `data/raw/`；产出 `quant/data/loader.py`
- [ ] **Day 3 | 收益率与累计收益** — 日收益率、累计收益曲线；产出 `quant/indicators/returns.py`
- [ ] **Day 4 | 波动率与回撤** — 年化波动率、最大回撤；产出 `quant/indicators/drawdown.py`
- [ ] **Day 5 | 绩效指标** — 夏普、年化收益、胜率、盈亏比；产出 `quant/indicators/metrics.py`
- [ ] **Day 6 (周末) | SMA / EMA / 布林带 / RSI** — 集中实现四个技术指标；产出 `quant/indicators/` 下对应文件
- [ ] **Day 7 (周末) | 验证 + 周复盘** — 用 3 个标的跑所有指标并画图验证；写 `docs/week01_report.md`

**代码示例：**

```python
import yfinance as yf

df = yf.download("SPY", start="2018-01-01", auto_adjust=True)
df["daily_return"] = df["Close"].pct_change()
df["cum_return"] = (1 + df["daily_return"]).cumprod()
df[["Close", "cum_return"]].plot(subplots=True)
```

```python
def add_sma(df, window: int, price_col="close"):
    df = df.copy()
    df[f"sma_{window}"] = df[price_col].rolling(window).mean()
    return df
```

---

## 第 2 周：回测引擎 + 第一个策略

> 目标：从零写回测器，跑通双均线策略，理解未来函数和交易成本。

- [ ] **Day 8 | 回测概念** — 理解 signal、position、equity、pnl、commission、slippage
- [ ] **Day 9 | 最小回测引擎** — 数据 → 信号 → 仓位 → 收益 → 权益曲线；产出 `quant/backtest/engine.py`
- [ ] **Day 10 | 双均线策略** — 5/20 日均线交叉，产出 `quant/strategies/ma_cross.py`
- [ ] **Day 11 | 未来函数 + 成本** — `shift(1)` 避免偷看；加手续费和滑点，对比前后差异
- [ ] **Day 12 | 绩效报告** — 输出总收益、年化、回撤、夏普、胜率；产出 `quant/report/report.py`
- [ ] **Day 13 (周末) | 多标的回测** — 跑 SPY、QQQ、BTC，观察策略在不同标的上的表现差异
- [ ] **Day 14 (周末) | 周复盘** — 写 `docs/week02_report.md`，总结回测器设计和双均线结果

**回测核心逻辑：**

```python
df["signal"] = (df["sma_5"] > df["sma_20"]).astype(int)
df["position"] = df["signal"].shift(1).fillna(0)   # 关键：避免未来函数
df["asset_return"] = df["close"].pct_change()
df["trade"] = df["position"].diff().abs().fillna(0)
df["strategy_return"] = df["position"] * df["asset_return"] - df["trade"] * 0.0005
df["equity"] = (1 + df["strategy_return"]).cumprod()
```

---

## 第 3 周：更多策略 + 风控

> 目标：实现 3 类策略，加上基础风控，建立"策略不是越赚钱越好，是要活得久"的认知。

- [ ] **Day 15 | 突破策略** — 突破 20 日高点买入，跌破 10 日低点卖出；产出 `quant/strategies/breakout.py`
- [ ] **Day 16 | 布林带均值回归** — 跌破下轨买入，回到中轨卖出；产出 `quant/strategies/bollinger_reversion.py`
- [ ] **Day 17 | 策略对比** — 双均线 vs 突破 vs 布林带，对比收益、回撤、交易频率
- [ ] **Day 18 | 止损 + 移动止损** — 固定止损 5%、移动止损从高点回撤 8%；产出 `quant/risk/stop_loss.py`
- [ ] **Day 19 | 仓位管理** — 测试 100% / 50% / 30% 仓位对收益和回撤的影响
- [ ] **Day 20 (周末) | 风控对比** — 无风控 vs 止损 vs 移动止损 vs 低仓位，出对比表
- [ ] **Day 21 (周末) | 周复盘** — 写 `docs/week03_report.md`，定下自己的风控策略

**策略认知框架：**

| 策略 | 核心假设 | 适合市场 | 主要风险 |
|------|---------|---------|---------|
| 双均线 | 趋势会延续 | 趋势市 | 震荡市反复亏 |
| 突破 | 创新高后继续涨 | 强趋势 | 假突破亏损 |
| 布林带 | 偏离均值会回归 | 震荡市 | 单边下跌接飞刀 |

---

## 第 4 周：报告 + 整合 + 复盘

> 目标：把前三周的零件装成一个完整系统，产出可展示的成果，想清楚下一步。

- [ ] **Day 22 | 配置化** — YAML 管理策略参数；产出 `configs/ma_cross_spy.yaml`
- [ ] **Day 23 | CLI 入口** — `python run_backtest.py --config configs/xxx.yaml` 一键回测
- [ ] **Day 24 | 自动报告** — 自动生成 Markdown 回测报告（指标 + 权益曲线 + 回撤图）；产出 `quant/report/generator.py`
- [ ] **Day 25 | 参数敏感性** — 测试 5/20、10/30、20/60 等参数组合，警惕单点最优
- [ ] **Day 26 | Walk-forward 测试** — 2018-2021 训练，2022-2023 验证，2024-至今测试
- [ ] **Day 27 (周末) | 完整回测合集** — 所有策略 × 有/无风控，生成完整报告
- [ ] **Day 28 (周末) | 最终复盘** — 写 `docs/final_report.md`，回答下面的问题
- [ ] **Day 29 | 代码整理** — 类型标注、README、清理无用文件
- [ ] **Day 30 | 下一步决策** — 确定接下来的方向

**最终复盘要回答的问题：**

1. 策略的收益来自哪里？在什么市场环境下有效？
2. 最大可能亏多少？能接受吗？
3. 哪些环节的理解还不够深？
4. 下一步是：深入因子研究 / 学习更多策略 / 模拟盘 / 做量化工具？

---

## 硬规则

- [ ] 不加杠杆
- [ ] 不因为单次回测好看就实盘
- [ ] 至少模拟盘 3 个月再考虑极小资金测试
- [ ] 每周必须写复盘

---

## 附录：工具与资料

### 工具栈

| 用途 | 推荐 | 说明 |
|------|------|------|
| Python 环境 | uv / conda | 少折腾 |
| IDE | Cursor / VS Code | 用 AI 辅助写模块 |
| 数据 | yfinance | 入门够用，SPY / QQQ / BTC |
| 可视化 | matplotlib | 够用，plotly 可选 |
| 回测 | 先手写 | 理解机制比用框架重要 |

### 安装

```bash
pip install pandas numpy matplotlib yfinance scipy pyyaml jupyterlab
```

> 前 2 周只用 pandas / numpy / matplotlib / yfinance。不要提前装量化框架。

### 学习资料（按需查）

| 场景 | 去哪 |
|------|------|
| 遇到术语不懂 | Investopedia 搜关键词 |
| 量化全景概念 | 《打开量化投资的黑箱》第 1-2 章 |
| pandas 操作 | 《Python for Data Analysis》看 rolling / groupby |
| 策略思路 | QuantStart 博客 |
| 中文快速入门 | B 站搜"量化交易 回测" |

### 搜索关键词

| 主题 | 关键词 |
|------|--------|
| 回测 | backtesting, lookahead bias, vectorized backtest |
| 指标 | moving average crossover, bollinger bands, RSI |
| 风险 | maximum drawdown, Sharpe ratio, position sizing, trailing stop |

### 每日验收

> **工作日（30 分钟）：** 完成一件事——写一个函数、画一张图、或写半页笔记。
>
> **周末（2-3 小时）：** 必须有可运行的代码产出 + 一次 commit。

---

## 30 天之后

完成这 30 天后，你已经具备了：
- 一个可运行的回测系统
- 3 个经典策略的实现和对比
- 基础风控能力
- 独立研究新策略的能力

后续可以按需扩展的方向（不用着急）：

| 方向 | 内容 |
|------|------|
| 因子研究 | 动量因子、波动率因子、因子排序回测 |
| 更多策略 | 动量轮动、配对交易、多因子组合 |
| Agent 集成 | LLM 自动总结回测报告、提实验建议 |
| 模拟盘 | 纸上交易规则、每日信号检查、模拟盘日志 |
| 统计深入 | 相关性、假设检验、过拟合检测 |
