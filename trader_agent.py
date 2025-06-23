# agents/trader_agent.py

import re
import streamlit as st
from langchain.tools import Tool
from services.alpaca_service import AlpacaService
from services.memory_service import MemoryService
from services.deepseek_service import DeepSeekService

memory = MemoryService()

def trade_stock(user_input: str) -> str:
    memory.log_user_input(user_input)

    # 1️⃣ Parse action, qty, symbol from user input
    match = re.search(r"(buy|sell)\s+(\d+)\s+([A-Za-z]+)", user_input.lower())
    if match:
        action, qty, symbol = match.groups()
    else:
        prompt = f"""
Extract trade intent in the format: <buy/sell> <quantity> <symbol>
User input: "{user_input}"
Strictly return one line in the exact format with no extra text.
"""
        response = DeepSeekService.ask_deepseek(prompt).strip().lower()
        match = re.search(r"(buy|sell)\s+(\d+)\s+([a-zA-Z]+)", response)
        if not match:
            return "❌ Could not parse trade command. Try 'buy 5 AAPL' or similar."
        action, qty, symbol = match.groups()

    # 2️⃣ Get Alpaca keys from session
    api_key = st.session_state.get("alpaca_key")
    secret_key = st.session_state.get("alpaca_secret")
    if not api_key or not secret_key:
        return "❌ Alpaca API keys not found in session. Please re-login."

    # 3️⃣ Execute trade
    result = AlpacaService.place_order(api_key, secret_key, symbol, int(qty), action)
    if "error" in result:
        return f"[Alpaca Error] {result['error']}"

    memory.log_trade(action, symbol.upper(), int(qty), result.get("status", "submitted"))
    return f"✅ Order placed: {action.upper()} {qty} shares of {symbol.upper()}"

trader_agent = Tool(
    name="TraderAgent",
    func=trade_stock,
    description="Use this to place trades like 'buy 5 AAPL' or 'sell 3 TSLA'."
)
