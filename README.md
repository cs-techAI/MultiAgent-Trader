# 🤖 SmartTrader — Langchain-Powered Autonomous Trading Assistant

SmartTrader is a multi-agent autonomous assistant built with **Langchain**, powered by **DeepSeek LLM**, and integrated with **Alpaca's trading API**.

It supports:
- 💬 Natural language chat interface
- 🧠 Multi-agent architecture (analyzer, trader, monitor)
- 📈 Real-time trading via Alpaca (paper trading)
- 📊 Portfolio dashboard with live order status
- 🧠 Persistent memory using SQLite
- 🔐 Ready for user login support (optional)

---

## 📁 Project Structure

langchain_smart_trader/
│
├── agents/ # Langchain tools (Analyzer, Trader, Monitor)
│ ├── analyzer_agent.py
│ ├── trader_agent.py
│ ├── monitor_agent.py
│ └── router_agent.py # Langchain agent executor
│
├── services/ # Business logic & APIs
│ ├── alpaca_service.py
│ ├── deepseek_service.py
│ ├── memory_service.py
│ └── portfolio_service.py
│
├── ui/
│ └── streamlit_app.py # Full Streamlit UI with chat + dashboard
│
├── .env # API keys (do not commit)
├── main.py # Optional CLI runner
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🔧 Setup Instructions

### 1. 🔐 Configure API Keys

Create a `.env` file:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets
2. 📦 Install Dependencies

pip install -r requirements.txt
3. 🚀 Run the App

streamlit run ui/streamlit_app.py
Or use the CLI (optional):

✨ Features
Agent	Description
AnalyzerAgent	Uses DeepSeek LLM to analyze stocks and give investment advice
TraderAgent	Places real trades using Alpaca paper trading API
MonitorAgent	Shows trade history, portfolio holdings, pending orders
RouterAgent	Langchain AgentExecutor that routes queries automatically

✅ Usage Examples
“Can I invest in Tesla now?”
→ SmartTrader uses AnalyzerAgent to give market insight.

“Buy 5 shares of AAPL”
→ SmartTrader routes to TraderAgent and executes live order.

“Show my portfolio”
→ SmartTrader calls MonitorAgent and shows holdings and trades.

🧱 Built With
Langchain

DeepSeek

Alpaca API

Streamlit