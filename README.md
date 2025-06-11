# 🤖 SmartTrader — Langchain-Powered Autonomous Trading Assistant

SmartTrader is an intelligent, multi-agent trading assistant built using **Langchain**, **DeepSeek LLM**, and **Streamlit**, with trading operations executed via the **Alpaca API**.

It provides:

* 💬 Natural language chat interface for analysis and trading
* 🧠 Multi-agent system: Analyzer, Trader, Monitor (orchestrated by Router)
* 📈 Real-time portfolio tracking via Alpaca
* 📊 Interactive dashboard with stock cards, charts, and suggestions
* 🧠 Persistent memory using SQLite
* 🔐 Custom login system (JSON + bcrypt)
* 🎨 Stylish UI with a responsive, colorful layout

---

## 📁 Project Structure

```
langchain_smart_trader/
│
├── agents/
│   ├── analyzer_agent.py        # Stock analysis via DeepSeek
│   ├── trader_agent.py          # Buy/sell stocks
│   ├── monitor_agent.py         # Portfolio and order insights
│   └── router_agent.py          # Langchain AgentExecutor & dispatcher
│
├── services/
│   ├── alpaca_service.py        # Order execution via Alpaca API
│   ├── auth_service.py          # Login system using bcrypt + JSON
│   ├── deepseek_service.py      # DeepSeek prompt interface
│   ├── memory_service.py        # SQLite memory store
│   ├── news_service.py          # Market news via Finnhub API
│   └── portfolio_service.py     # Holdings and orders from Alpaca
│
├── ui/
│   └── streamlit_app.py         # Streamlit front-end for chat + dashboard
│
├── .env                         # Environment variables
├── main.py                      # Optional CLI interface
├── requirements.txt             # All dependencies
└── README.md                    # Project overview
```

---

## 🔧 Setup Instructions

### 1. 🔐 Environment Configuration

Create a `.env` file in root:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets
FINNHUB_API_KEY=your_finnhub_api_key
```

### 2. 📦 Install Requirements

```bash
pip install -r requirements.txt
```

### 3. 🚀 Run the Streamlit App

```bash
streamlit run ui/streamlit_app.py
```

---

## ✨ Features & Agents

| Agent             | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| `AnalyzerAgent`   | Uses DeepSeek to analyze stocks and recommend Buy/Hold/Sell      |
| `TraderAgent`     | Parses trade instructions and executes them on Alpaca            |
| `MonitorAgent`    | Fetches and displays portfolio, open orders, and trade history   |
| `RouterAgent`     | LLM-powered dispatcher that routes messages to the correct agent |
| `DeepSeekService` | LLM handler for symbol extraction, follow-ups, and suggestions   |

## 🧠 Agentic Flow Examples

* "Should I buy Tesla?"
  → `RouterAgent` → `AnalyzerAgent` → Analysis + prompt: "Want to invest?"

* "Buy 10 AAPL"
  → `RouterAgent` → `TraderAgent` → Alpaca order placed

* "Show my positions"
  → `RouterAgent` → `MonitorAgent` → Table and charts

* "View details" → (UI)
  → Bull/Bear perspective loaded from DeepSeek

---

## 🎨 UI Highlights

* Color-coded stock performance cards (green/red)
* Suggested stocks user doesn’t own
* View Details + Buy popup flow
* Interactive pie and bar charts
* Stylish gradient backgrounds and dark sidebar

---

## ✅ Requirements

### `requirements.txt`

```
bcrypt
streamlit
plotly
pandas
requests
openai
python-dotenv
langchain
tqdm
```

---

## 🧱 Built With

* [Langchain](https://github.com/hwchase17/langchain)
* [DeepSeek](https://deepseek.com)
* [Streamlit](https://streamlit.io)
* [Alpaca Markets API](https://alpaca.markets)
* [Finnhub API](https://finnhub.io)

---

## 📬 Contact / Contributions

Pull requests and feedback are welcome!

---

## 📌 License

This project is open-sourced for educational and prototyping use.
