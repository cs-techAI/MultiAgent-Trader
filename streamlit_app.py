# ui/streamlit_app.py

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



st.set_page_config(page_title="SmartTrader", layout="wide")
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
                st.error("Invalid credentials.")

else:
    st.sidebar.success(f"Welcome, {st.session_state.user} 👋")
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()

    tab = st.sidebar.radio("Choose view:", ["🤖 Chat", "📊 Portfolio Dashboard"])

    if "router" not in st.session_state:
        st.session_state.router = RouterAgent()
        st.session_state.chat_history = []





    # ------------------- 🤖 Chat -------------------
    if tab == "🤖 Chat":
        st.markdown("### 💬 Chat with SmartTrader")

        for speaker, message in st.session_state.chat_history:
            if speaker == "You":
                st.markdown(f"<div style='text-align:right;background-color:#d2e8ff;padding:10px 15px;border-radius:10px;margin:5px 0 10px 30%;max-width:70%;float:right;clear:both'><strong>🧑 You:</strong><br>{message}</div>", unsafe_allow_html=True)
            else:
                content, agent_used = message
                st.markdown(f"<div style='text-align:left;background-color:#eeeeee;padding:10px 15px;border-radius:10px;margin:5px 30% 10px 0;max-width:70%;float:left;clear:both'><strong>🤖 SmartTrader <span style='font-size:12px'>({agent_used})</span>:</strong><br>{content}</div>", unsafe_allow_html=True)

        user_input = st.chat_input("Ask anything about stocks, trades, or portfolio...")



        if user_input:
            st.session_state.chat_history.append(("You", user_input))

            if "investment_flow" in st.session_state:
                flow = st.session_state["investment_flow"]
                context = flow.get("context", "")
                result = DeepSeekService.handle_investment_followup(context, user_input)

                action = result.get("action")
                msg = result.get("message", "")
                symbol = result.get("symbol", flow.get("symbol"))
                qty = result.get("quantity", flow.get("quantity"))



                if action == "ask_quantity":
                    st.session_state["investment_flow"] = {
                        "step": "awaiting_quantity",
                        "symbol": symbol,
                        "context": context + f"\nUser: {user_input}\nAssistant: {msg}"
                    }
                    st.session_state.chat_history.append(("SmartTrader", (msg, "SmartTrader")))
                    st.rerun()

                elif action == "ask_confirmation":
                    st.session_state["investment_flow"] = {
                        "step": "awaiting_confirmation",
                        "symbol": symbol,
                        "quantity": qty,
                        "context": context + f"\nUser: {user_input}\nAssistant: {msg}"
                    }
                    st.session_state.chat_history.append(("SmartTrader", (msg, "SmartTrader")))
                    st.rerun()


                elif action == "execute_trade":
                    command = f"buy {qty} {symbol}"
                    response, used = st.session_state.router.route(command)
                    st.session_state.chat_history.append(("SmartTrader", (response, "TraderAgent")))
                    del st.session_state["investment_flow"]
                    st.rerun()

                elif action == "cancel":
                    del st.session_state["investment_flow"]
                    st.session_state.chat_history.append(("SmartTrader", ("Got it. Trade cancelled.", "SmartTrader")))
                    st.rerun()

                else:
                    st.session_state.chat_history.append(("SmartTrader", (msg, "SmartTrader")))
                    st.rerun()

            else:
                response, agent_used = st.session_state.router.route(user_input)

                if agent_used == "AnalyzerAgent":
                    symbol = DeepSeekService.extract_stock_symbol(user_input)
                    if symbol:
                        followup = f"Would you like to invest in {symbol} now?"
                        st.session_state["investment_flow"] = {
                            "step": "awaiting_investment_decision",
                            "symbol": symbol,
                            "context": response + f"\n\nAssistant: {followup}"
                        }
                        response += f"\n\n🤖 {followup}"

                st.session_state.chat_history.append(("SmartTrader", (response, agent_used)))
                st.rerun()




    # ------------------- 📊 Dashboard -------------------
    elif tab == "📊 Portfolio Dashboard":
        st.subheader("📦 Current Holdings")
        positions = PortfolioService.get_positions()

        if "error" in positions:
            st.error(f"Failed to load portfolio: {positions['error']}")


        elif not positions:
            st.info("No open positions found.")

        else:
            df = pd.DataFrame(positions)
            df = df[["symbol", "qty", "avg_entry_price", "market_value", "unrealized_pl", "unrealized_plpc"]]
            df.columns = ["Symbol", "Qty", "Avg Price", "Market Value", "Unrealized P/L", "Unrealized %"]
            df["Market Value"] = df["Market Value"].astype(float)
            df["Unrealized P/L"] = df["Unrealized P/L"].astype(float)
            df["Unrealized %"] = df["Unrealized %"].astype(float).map(lambda x: f"{x:.2%}")
            st.dataframe(df, use_container_width=True)



            st.subheader("📈 Portfolio Allocation")
            fig_pie = px.pie(df, names="Symbol", values="Market Value")
            st.plotly_chart(fig_pie, use_container_width=True)


            st.subheader("📈 Unrealized Gains / Losses")
            fig_bar = px.bar(df, x="Symbol", y="Unrealized P/L")
            st.plotly_chart(fig_bar, use_container_width=True)




            st.divider()
            st.subheader("🗞️ Market Headlines")
            for article in NewsService.get_market_news():
                st.markdown(f"- [{article['headline']}]({article.get('url', '#')})")



            st.divider()
            st.subheader("💡 Stock Suggestions")
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
