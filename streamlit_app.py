import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px

from services.auth_service import authenticate_user, register_user
from services.portfolio_service import PortfolioService
from services.deepseek_service import DeepSeekService
from services.news_service import NewsService
from agents.router_agent import RouterAgent
from agents.trader_agent import trade_stock

st.set_page_config(page_title="SmartTrader", layout="wide")

# Inject colorful background and card styles
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(to right, #f5f7fa, #c3cfe2);
    font-family: 'Segoe UI', sans-serif;
}
.sidebar .sidebar-content {
    background-color: #2f3e46;
    color: white;
}
.stock-box {
    padding: 1em;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    margin: 0.5em;
}
.green { background: #d4edda; color: #155724; }
.red { background: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

st.title("📈 SmartTrader Assistant")

# -------------------- Login / Signup --------------------
if "user" not in st.session_state:
    auth_mode = st.radio("Login or Signup", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_mode == "Signup":
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("Create Account"):
            if password != confirm:
                st.error("Passwords do not match.")
            else:
                success, msg = register_user(username, password)
                st.success(msg) if success else st.error(msg)

    else:
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.user = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")

else:
    st.sidebar.success(f"Welcome, {st.session_state.user} 👋")
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()

    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "detail_symbol" not in st.session_state:
        st.session_state.detail_symbol = None
    if "buying_symbol" not in st.session_state:
        st.session_state.buying_symbol = None

    if st.session_state.page == "details":
        symbol = st.session_state.detail_symbol
        st.subheader(f"🔍 Detailed Analysis for {symbol}")
        bull = DeepSeekService.ask_deepseek(f"Why is {symbol} good to buy short-term?")
        bear = DeepSeekService.ask_deepseek(f"What are the risks of holding {symbol} long-term?")
        st.markdown(f"**📈 Bullish View:** {bull}")
        st.markdown(f"**📉 Bearish View:** {bear}")
        if st.button("🔙 Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.session_state.detail_symbol = None
            st.rerun()

    elif st.session_state.page == "dashboard":
        tab = st.sidebar.radio("Choose view:", ["📊 Portfolio Dashboard", "🤖 Chat"])

        if "router" not in st.session_state:
            st.session_state.router = RouterAgent()
            st.session_state.chat_history = []

        if tab == "📊 Portfolio Dashboard":
            positions = PortfolioService.get_positions()

            if "error" in positions:
                st.error(f"Failed to load portfolio: {positions['error']}")
            elif not positions:
                st.info("No open positions found.")
            else:
                df = pd.DataFrame(positions)
                df = df[["symbol", "qty", "avg_entry_price", "market_value", "unrealized_pl", "unrealized_plpc", "current_price"]]
                df.columns = ["Symbol", "Qty", "Avg Price", "Market Value", "Unrealized P/L", "Unrealized %", "Price"]
                df = df.astype({"Market Value": float, "Unrealized P/L": float, "Unrealized %": float, "Price": float})

                st.markdown("## 📊 Your Stock Performance")
                cols = st.columns(len(df))
                for i, row in df.iterrows():
                    pct = float(row["Unrealized %"])
                    color = "green" if pct >= 0 else "red"
                    sign = "▲" if pct >= 0 else "▼"
                    label = f"{row['Symbol']}<br>${row['Price']:.2f} {sign} ({pct:.2f}%)"
                    cols[i].markdown(f"<div class='stock-box {color}'>{label}</div>", unsafe_allow_html=True)

                st.divider()
                st.subheader("🔍 Suggested Stocks You Don't Own")
                st.markdown("Here are some high-performing stocks you don't hold:")

                held_symbols = set(df["Symbol"].unique())
                all_top_stocks = ["MSFT", "AMZN", "NFLX", "NVDA", "TSLA", "GOOG"]
                candidates = [s for s in all_top_stocks if s not in held_symbols][:3]

                for symbol in candidates:
                    with st.container():
                        st.markdown(f"### 📈 {symbol}")
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button(f"📋 View Details - {symbol}"):
                                st.session_state.page = "details"
                                st.session_state.detail_symbol = symbol
                                st.rerun()
                        with col2:
                            if st.button(f"💸 Buy - {symbol}"):
                                st.session_state.buying_symbol = symbol

                        if st.session_state.buying_symbol == symbol:
                            qty = st.number_input(f"How many shares of {symbol} to buy?", min_value=1, step=1, key=f"qty_{symbol}")
                            if st.button(f"✅ Confirm Buy {symbol}"):
                                result = trade_stock(f"buy {qty} {symbol}")
                                st.success(result)
                                st.session_state.buying_symbol = None

                st.divider()
                st.subheader("📆 Current Holdings")
                st.dataframe(df[["Symbol", "Qty", "Avg Price", "Market Value", "Unrealized P/L", "Unrealized %"]], use_container_width=True)

                st.divider()
                st.subheader("🗳️ Market Headlines")
                for article in NewsService.get_market_news():
                    st.markdown(f"- [{article['headline']}]({article.get('url', '#')})")

                st.divider()
                st.subheader("📈 Portfolio Charts")
                pie = px.pie(df, names="Symbol", values="Market Value", title="💰 Portfolio Allocation by Value")
                st.plotly_chart(pie, use_container_width=True)

                bar = px.bar(df, x="Symbol", y="Unrealized P/L", title="📉 Unrealized Profit & Loss")
                st.plotly_chart(bar, use_container_width=True)

                st.divider()
                st.subheader("💡 Suggestions")
                for sym in df["Symbol"]:
                    suggestion = DeepSeekService.suggest_action_for_stock(sym)
                    st.markdown(f"**{sym}** → {suggestion}")

                st.divider()
                st.subheader("⏳ Pending Orders")
                orders = PortfolioService.get_open_orders()
                if "error" in orders:
                    st.error(f"Failed to load orders: {orders['error']}")
                elif not orders:
                    st.info("No pending orders.")
                else:
                    df_orders = pd.DataFrame(orders)
                    df_orders = df_orders[["symbol", "qty", "side", "type", "status", "submitted_at"]]
                    df_orders.columns = ["Symbol", "Qty", "Side", "Type", "Status", "Submitted At"]
                    st.dataframe(df_orders, use_container_width=True)

        elif tab == "🤖 Chat":
            st.markdown("### 💬 Chat with SmartTrader")
            chat_container = st.container()

            for speaker, message in st.session_state.chat_history:
                if speaker == "You":
                    st.markdown(f"<div style='text-align:right;background-color:#d2e8ff;padding:10px 15px;border-radius:10px;margin:5px 0 10px 30%;max-width:70%;float:right;clear:both'><strong>🧑 You:</strong><br>{message}</div>", unsafe_allow_html=True)
                else:
                    content, agent_used = message
                    st.markdown(f"<div style='text-align:left;background-color:#eeeeee;padding:10px 15px;border-radius:10px;margin:5px 30% 10px 0;max-width:70%;float:left;clear:both'><strong>🤖 SmartTrader <span style='font-size:12px'>({agent_used})</span>:</strong><br>{content}</div>", unsafe_allow_html=True)

            user_input = st.chat_input("Ask anything about stocks, trades, or portfolio...")
            if user_input:
                st.session_state.chat_history.append(("You", user_input))
                response, agent_used = st.session_state.router.route(user_input)
                st.session_state.chat_history.append(("SmartTrader", (response, agent_used)))
                st.rerun()
