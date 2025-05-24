# AI Hedge Fund

This is a proof of concept for an AI-powered hedge fund.  The goal of this project is to explore the use of AI to make trading decisions.  This project is for **educational** purposes only and is not intended for real trading or investment.

This system employs several agents working together:

1. Aswath Damodaran Agent - The Dean of Valuation, focuses on story, numbers, and disciplined valuation
2. Ben Graham Agent - The godfather of value investing, only buys hidden gems with a margin of safety
3. Bill Ackman Agent - An activist investor, takes bold positions and pushes for change
4. Cathie Wood Agent - The queen of growth investing, believes in the power of innovation and disruption
5. Charlie Munger Agent - Warren Buffett's partner, only buys wonderful businesses at fair prices
6. Michael Burry Agent - The Big Short contrarian who hunts for deep value
7. Peter Lynch Agent - Practical investor who seeks "ten-baggers" in everyday businesses
8. Phil Fisher Agent - Meticulous growth investor who uses deep "scuttlebutt" research 
9. Stanley Druckenmiller Agent - Macro legend who hunts for asymmetric opportunities with growth potential
10. Warren Buffett Agent - The oracle of Omaha, seeks wonderful companies at a fair price
11. Valuation Agent - Calculates the intrinsic value of a stock and generates trading signals
12. Sentiment Agent - Analyzes market sentiment and generates trading signals
13. Fundamentals Agent - Analyzes fundamental data and generates trading signals
14. Technicals Agent - Analyzes technical indicators and generates trading signals
15. Risk Manager - Calculates risk metrics and sets position limits
16. Portfolio Manager - Makes final trading decisions and generates orders
    
<img width="1042" alt="Screenshot 2025-03-22 at 6 19 07 PM" src="https://github.com/user-attachments/assets/cbae3dcf-b571-490d-b0ad-3f0f035ac0d4" />


**Note**: the system simulates trading decisions, it does not actually trade.

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [Setup](#setup)
  - [Using Poetry](#using-poetry)
  - [Using Docker](#using-docker)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Feature Requests](#feature-requests)
- [License](#license)

## Setup

### Using Poetry

Clone the repository:
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env
```

4. Set your API keys:
```bash
# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
# Get your OpenAI API key from https://platform.openai.com/
OPENAI_API_KEY=your-openai-api-key

# For running LLMs hosted by groq (deepseek, llama3, etc.)
# Get your Groq API key from https://groq.com/
GROQ_API_KEY=your-groq-api-key

# For getting financial data to power the hedge fund
# Get your Financial Datasets API key from https://financialdatasets.ai/
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

### Using Docker

1. Make sure you have Docker installed on your system. If not, you can download it from [Docker's official website](https://www.docker.com/get-started).

2. Clone the repository:
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env
```

4. Edit the .env file to add your API keys as described above.

5. Build the Docker image:
```bash
# On Linux/Mac:
./run.sh build

# On Windows:
run.bat build
```

**Important**: You must set `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY` for the hedge fund to work.  If you want to use LLMs from all providers, you will need to set all API keys.

Financial data for AAPL, GOOGL, MSFT, NVDA, and TSLA is free and does not require an API key.

For any other ticker, you will need to set the `FINANCIAL_DATASETS_API_KEY` in the .env file.

## Usage

### Running the Hedge Fund

#### With Poetry
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

#### With Docker
```bash
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA main

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA main
```

**Example Output:**
<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

You can also specify a `--ollama` flag to run the AI hedge fund using local LLMs.

```bash
# With Poetry:
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --ollama

# With Docker (on Linux/Mac):
./run.sh --ticker AAPL,MSFT,NVDA --ollama main

# With Docker (on Windows):
run.bat --ticker AAPL,MSFT,NVDA --ollama main
```

You can also specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
# With Poetry:
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning

# With Docker (on Linux/Mac):
./run.sh --ticker AAPL,MSFT,NVDA --show-reasoning main

# With Docker (on Windows):
run.bat --ticker AAPL,MSFT,NVDA --show-reasoning main
```

You can optionally specify the start and end dates to make decisions for a specific time period.

```bash
# With Poetry:
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 

# With Docker (on Linux/Mac):
./run.sh --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 main

# With Docker (on Windows):
run.bat --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 main
```

### Running the Backtester

#### With Poetry
```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

#### With Docker
```bash
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA backtest

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA backtest
```

**Example Output:**
<img width="941" alt="Screenshot 2025-01-06 at 5 47 52 PM" src="https://github.com/user-attachments/assets/00e794ea-8628-44e6-9a84-8f8a31ad3b47" />


You can optionally specify the start and end dates to backtest over a specific time period.

```bash
# With Poetry:
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01

# With Docker (on Linux/Mac):
./run.sh --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 backtest

# With Docker (on Windows):
run.bat --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 backtest
```

You can also specify a `--ollama` flag to run the backtester using local LLMs.
```bash
# With Poetry:
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --ollama

# With Docker (on Linux/Mac):
./run.sh --ticker AAPL,MSFT,NVDA --ollama backtest

# With Docker (on Windows):
run.bat --ticker AAPL,MSFT,NVDA --ollama backtest
```



## Project Structure 
```
ai-hedge-fund/
├── src/
│   ├── agents/                   # Agent definitions and workflow
│   │   ├── bill_ackman.py        # Bill Ackman agent
│   │   ├── fundamentals.py       # Fundamental analysis agent
│   │   ├── portfolio_manager.py  # Portfolio management agent
│   │   ├── risk_manager.py       # Risk management agent
│   │   ├── sentiment.py          # Sentiment analysis agent
│   │   ├── technicals.py         # Technical analysis agent
│   │   ├── valuation.py          # Valuation analysis agent
│   │   ├── ...                   # Other agents
│   │   ├── warren_buffett.py     # Warren Buffett agent
│   │   ├── aswath_damodaran.py   # Aswath Damodaran agent
│   │   ├── ...                   # Other agents
│   │   ├── ...                   # Other agents
│   ├── tools/                    # Agent tools
│   │   ├── api.py                # API tools
│   ├── backtester.py             # Backtesting tools
│   ├── main.py # Main entry point
├── pyproject.toml
├── ...
```

## Prompt Templates

### English

Below are the prompt templates and their variable placeholders:

- **Template 1: warren_buffett_agent**  
  - **System**: Fixed role description for a Warren Buffett AI agent.  
  - **Human**:  
    ```  
    Based on the following data, create the investment signal as Warren Buffett would:

    Analysis Data for {{TICKER}}:
    {{ANALYSIS_JSON}}

    Return the trading signal in the following JSON format exactly:
    {
      "signal": "bullish" | "bearish" | "neutral",
      "confidence": float between 0 and 100,
      "reasoning": "string"
    }
    ```  
  - **Variables**:  
    - `{{TICKER}}`: stock ticker symbol  
    - `{{ANALYSIS_JSON}}`: JSON object with financial metrics and scores  

- **Template 2: portfolio_manager**  
  - **System**: Fixed role description for a portfolio manager agent.  
  - **Human**:  
    ```  
    Based on the team's analysis, make your trading decisions for each ticker.

    Here are the signals by ticker:
    {{SIGNALS_JSON}}

    Current Prices:
    {{PRICES_JSON}}

    Maximum Shares Allowed For Purchases:
    {{MAX_SHARES_JSON}}

    Portfolio Cash: {{CASH}}
    Current Positions: {{POSITIONS_JSON}}
    Current Margin Requirement: {{MARGIN_REQ}}
    Total Margin Used: {{MARGIN_USED}}

    Output strictly in JSON with the following structure:
    {
      "decisions": { … }
    }
    ```  
  - **Variables**:  
    - `{{SIGNALS_JSON}}`, `{{PRICES_JSON}}`, `{{MAX_SHARES_JSON}}`  
    - `{{CASH}}`, `{{POSITIONS_JSON}}`, `{{MARGIN_REQ}}`, `{{MARGIN_USED}}`

### 提示模板（中文）

以下是提示模板及其变量位置说明：

- **模板 1：warren_buffett_agent**  
  - **System**：固定的角色描述，定位为 Warren Buffett AI 代理。  
  - **Human**：  
    ```  
    根据以下数据，按 Warren Buffett 的方式生成投资信号：

    分析数据 - {{TICKER}}:
    {{ANALYSIS_JSON}}

    严格按照以下 JSON 格式返回信号：
    {
      "signal": "bullish" | "bearish" | "neutral",
      "confidence": 0 到 100 之间的浮点数,
      "reasoning": "原因说明"
    }
    ```  
  - **变量**：  
    - `{{TICKER}}`：股票代码  
    - `{{ANALYSIS_JSON}}`：包含财务指标和评分的 JSON 对象  

- **模板 2：portfolio_manager**  
  - **System**：固定的角色描述，定位为投资组合管理代理。  
  - **Human**：  
    ```  
    根据团队的分析，为每个股票做出交易决策。

    各股票信号：
    {{SIGNALS_JSON}}

    当前价格：
    {{PRICES_JSON}}

    可买入最大股数：
    {{MAX_SHARES_JSON}}

    账户现金：{{CASH}}
    当前持仓：{{POSITIONS_JSON}}
    保证金要求：{{MARGIN_REQ}}
    已使用保证金：{{MARGIN_USED}}

    严格输出以下结构的 JSON：
    {
      "decisions": { … }
    }
    ```  
  - **变量**：  
    - `{{SIGNALS_JSON}}`、`{{PRICES_JSON}}`、`{{MAX_SHARES_JSON}}`  
    - `{{CASH}}`、`{{POSITIONS_JSON}}`、`{{MARGIN_REQ}}`、`{{MARGIN_USED}}`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused.  This will make it easier to review and merge.

## Feature Requests

If you have a feature request, please open an [issue](https://github.com/virattt/ai-hedge-fund/issues) and make sure it is tagged with `enhancement`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 中文翻译

# AI 对冲基金

这是一个基于 AI 的对冲基金概念验证。该项目的目标是探索使用 AI 来做出交易决策。此项目仅用于**教育**目的，不用于实际交易或投资。

该系统采用多个代理协同工作：

1. Aswath Damodaran 代理 - 估值大师，专注于故事、数字和严格的估值
2. Ben Graham 代理 - 价值投资教父，只购买带有安全边际的隐藏宝石
3. Bill Ackman 代理 - 激进投资者，采取大胆立场并推动变革
4. Cathie Wood 代理 - 成长投资女王，相信创新和颠覆的力量
5. Charlie Munger 代理 - Warren Buffett 的合伙人，只购买价格合理的优质企业
6. Michael Burry 代理 - 《大空头》逆向投资者，寻找深度价值
7. Peter Lynch 代理 - 实用投资者，寻找日常业务中的“十倍股”
8. Phil Fisher 代理 - 严谨的成长投资者，使用深入的“传闻”调研
9. Stanley Druckenmiller 代理 - 宏观传奇，寻找具有成长潜力的不对称机会
10. Warren Buffett 代理 - 奥马哈先知，寻找价格合理的优质公司
11. 估值代理 - 计算股票的内在价值并生成交易信号
12. 情绪代理 - 分析市场情绪并生成交易信号
13. 基本面代理 - 分析基本面数据并生成交易信号
14. 技术面代理 - 分析技术指标并生成交易信号
15. 风险管理者 - 计算风险指标并设置持仓限制
16. 投资组合经理 - 做出最终交易决策并生成订单

**注意**：该系统模拟交易决策，不进行实际交易。

## 免责声明

本项目仅用于**教育和研究目的**。

- 不用于实际交易或投资
- 不提供任何保证或担保
- 过去表现不代表未来结果
- 创作者不承担任何财务损失责任
- 投资决策请咨询专业财务顾问

使用本软件即表示您同意仅将其用于学习目的。

## 目录
- [安装](#安装)
  - [使用 Poetry](#使用-poetry)
  - [使用 Docker](#使用-docker)
- [使用方法](#使用方法)
  - [运行对冲基金](#运行对冲基金)
  - [运行回测器](#运行回测器)
- [项目结构](#项目结构)
- [贡献指南](#贡献指南)
- [功能请求](#功能请求)
- [许可证](#许可证)

## 安装

### 使用 Poetry

克隆仓库：
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

1. 安装 Poetry（如果尚未安装）：
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. 安装依赖：
```bash
poetry install
```

3. 设置环境变量：
```bash
# 创建 .env 文件以存放您的 API 密钥
cp .env.example .env
```

4. 设置您的 API 密钥：
```bash
# 用于运行由 openai 托管的 LLM（如 gpt-4o、gpt-4o-mini 等）
# 请从 https://platform.openai.com/ 获取您的 OpenAI API 密钥
OPENAI_API_KEY=your-openai-api-key

# 用于运行由 groq 托管的 LLM（如 deepseek、llama3 等）
# 请从 https://groq.com/ 获取您的 Groq API 密钥
GROQ_API_KEY=your-groq-api-key

# 用于获取金融数据以支持对冲基金
# 请从 https://financialdatasets.ai/ 获取您的 Financial Datasets API 密钥
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

### 使用 Docker

1. 确保您的系统已安装 Docker。如果没有，可以从 [Docker 官方网站](https://www.docker.com/get-started) 下载。

2. 克隆仓库：
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

3. 设置环境变量：
```bash
# 创建 .env 文件以存放您的 API 密钥
cp .env.example .env
```

4. 编辑 .env 文件，添加上述 API 密钥。

5. 构建 Docker 镜像：
```bash
# Linux/Mac 系统：
./run.sh build

# Windows 系统：
run.bat build
```

**重要**：必须设置 `OPENAI_API_KEY`、`GROQ_API_KEY`、`ANTHROPIC_API_KEY` 或 `DEEPSEEK_API_KEY`，对冲基金才能正常运行。如果想使用所有提供商的 LLM，需要设置所有 API 密钥。

AAPL、GOOGL、MSFT、NVDA 和 TSLA 的金融数据免费且无需 API 密钥。

其他股票代码需要在 .env 文件中设置 `FINANCIAL_DATASETS_API_KEY`。

## 使用方法

### 运行对冲基金

#### 使用 Poetry
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

#### 使用 Docker
```bash
# Linux/Mac 系统：
./run.sh --ticker AAPL,MSFT,NVDA main

# Windows 系统：
run.bat --ticker AAPL,MSFT,NVDA main
```

**示例输出：**
<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

您也可以使用 `--ollama` 参数，使用本地 LLM 运行 AI 对冲基金。

```bash
# 使用 Poetry：
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --ollama

# Linux/Mac Docker：
./run.sh --ticker AAPL,MSFT,NVDA --ollama main

# Windows Docker：
run.bat --ticker AAPL,MSFT,NVDA --ollama main
```

您还可以使用 `--show-reasoning` 参数，将每个代理的推理过程打印到控制台。

```bash
# 使用 Poetry：
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning

# Linux/Mac Docker：
./run.sh --ticker AAPL,MSFT,NVDA --show-reasoning main

# Windows Docker：
run.bat --ticker AAPL,MSFT,NVDA --show-reasoning main
```

您可以选择指定起始和结束日期，以针对特定时间段做出决策。

```bash
# 使用 Poetry：
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 

# Linux/Mac Docker：
./run.sh --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 main

# Windows Docker：
run.bat --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 main
```

### 运行回测器

#### 使用 Poetry
```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

#### 使用 Docker
```bash
# Linux/Mac 系统：
./run.sh --ticker AAPL,MSFT,NVDA backtest

# Windows 系统：
run.bat --ticker AAPL,MSFT,NVDA backtest
```

**示例输出：**
<img width="941" alt="Screenshot 2025-01-06 at 5 47 52 PM" src="https://github.com/user-attachments/assets/00e794ea-8628-44e6-9a84-8f8a31ad3b47" />

您可以选择指定起始和结束日期，对特定时间段进行回测。

```bash
# 使用 Poetry：
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01

# Linux/Mac Docker：
./run.sh --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 backtest

# Windows Docker：
run.bat --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 backtest
```

您也可以使用 `--ollama` 参数，使用本地 LLM 运行回测器。

```bash
# 使用 Poetry：
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --ollama

# Linux/Mac Docker：
./run.sh --ticker AAPL,MSFT,NVDA --ollama backtest

# Windows Docker：
run.bat --ticker AAPL,MSFT,NVDA --ollama backtest
```

## 项目结构 
```
ai-hedge-fund/
├── src/
│   ├── agents/                   # 代理定义和工作流程
│   │   ├── bill_ackman.py        # Bill Ackman 代理
│   │   ├── fundamentals.py       # 基本面分析代理
│   │   ├── portfolio_manager.py  # 投资组合管理代理
│   │   ├── risk_manager.py       # 风险管理代理
│   │   ├── sentiment.py          # 情绪分析代理
│   │   ├── technicals.py         # 技术分析代理
│   │   ├── valuation.py          # 估值分析代理
│   │   ├── ...                   # 其他代理
│   │   ├── warren_buffett.py     # Warren Buffett 代理
│   │   ├── aswath_damodaran.py   # Aswath Damodaran 代理
│   │   ├── ...                   # 其他代理
│   │   ├── ...                   # 其他代理
│   ├── tools/                    # 代理工具
│   │   ├── api.py                # API 工具
│   ├── backtester.py             # 回测工具
│   ├── main.py                   # 主入口
├── pyproject.toml
├── ...
```

## 贡献指南

1. Fork 本仓库
2. 创建功能分支
3. 提交您的更改
4. 推送到分支
5. 创建 Pull Request

**重要**：请保持您的 Pull Request 小且专注，这样更容易审查和合并。

## 功能请求

如果您有功能请求，请打开一个 [issue](https://github.com/virattt/ai-hedge-fund/issues)，并确保标签为 `enhancement`。

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。
