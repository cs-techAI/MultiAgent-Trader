## 🚀 Overview

SmartTrader is a **multi-agent financial assistant** that enables:

- 🧠 AI-powered stock analysis
- 📊 Real-time portfolio monitoring
- 💸 Trade execution via Alpaca (paper)
- 📰 Latest market news
- 🔐 Secure multi-user login/signup with custom API keys

---

## 📦 Features

| Feature                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| 🔐 Login & Signup          | Secure authentication with Alpaca API key storage                          |
| 💬 Chat Assistant          | Ask stock-related questions using natural language                         |
| 📈 Portfolio Dashboard     | View current holdings, unrealized gains, charts                            |
| 📉 Trading Agent           | Place real trades via Alpaca Paper API (buy/sell)                          |
| 📰 News Section            | Latest financial headlines via Finnhub                                     |
| 💡 Smart Suggestions       | Buy/Sell/Hold recommendations for each stock you own                       |

---

## 🛠️ Installation

### 1. Clone the repository

```bash

1. Set up virtual environment
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔐 Environment Setup
Create a .env file in the root directory with the following content:

env
Copy
Edit
DEEPSEEK_API_KEY=your_deepseek_key_here
FINNHUB_API_KEY=your_finnhub_key_here
💡 DeepSeek is used for stock analysis and follow-ups. Finnhub provides market headlines.

🚦 Usage
Launch the app locally:

bash
Copy
Edit
streamlit run ui/streamlit_app_1.py
Open http://localhost:8501 in your browser.

🧾 Folder Structure
bash
Copy
Edit
smarttrader/
│
├── agents/
│   ├── analyzer_agent.py         # Handles stock analysis
│   ├── monitor_agent.py          # Monitors portfolio and logs
│   ├── router_agent.py           # Routes queries to the right agent
│   └── trader_agent.py           # Handles stock trading
│
├── services/
│   ├── alpaca_service.py         # Communicates with Alpaca API
│   ├── auth_service.py           # Handles user registration/login
│   ├── deepseek_service.py       # Handles LLM responses and follow-up logic
│   ├── memory_service.py         # Tracks chat & trade history
│   ├── news_service.py           # Fetches news from Finnhub
│   └── portfolio_service.py      # Loads portfolio positions and orders
│
├── ui/
│   └── streamlit_app_1.py        # Streamlit front-end interface
│
├── user_db.json                  # Stores user credentials and Alpaca keys
├── .env                          # API keys (not checked into Git)
└── requirements.txt              # All Python dependencies
🧠 Technologies Used
✅ Streamlit — UI & dashboard

🧠 DeepSeek — LLM for investment logic

📊 Alpaca — Paper trading API

🛠️ LangChain — Agent orchestration

📰 Finnhub — News API


📌 Notes
This app uses Alpaca Paper API (no real trades).

All data is stored locally in user_db.json and session_state.

📝 License
Licensed under the MIT License. See LICENSE for more info.


🔗 Related Projects
LangChain

Streamlit

yaml
Copy
Edit

---

## ✅ Matching `requirements.txt`

```txt
streamlit==1.35.0
pandas
plotly
requests
python-dotenv
openai
langchain==0.3.14
langchain-openai==0.1.6
pydantic==1.10.14
streamlit-authenticator==0.3.2
