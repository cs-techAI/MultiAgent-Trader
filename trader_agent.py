# agents/trader_agent.py

import re
from langchain.tools import Tool
from services.alpaca_service import AlpacaService
from services.memory_service import MemoryService
from services.deepseek_service import DeepSeekService



memory = MemoryService()



def trade_stock(user_input: str) -> str:
    memory.log_user_input(user_input)

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



    result = AlpacaService.place_order(symbol=symbol, qty=int(qty), side=action)
    if "error" in result:
        return f"[Alpaca Error] {result['error']}"
    

    memory.log_trade(action, symbol.upper(), int(qty), result.get("status", "submitted"))
    return f"✅ Order placed: {action.upper()} {qty} shares of {symbol.upper()}"

trader_agent = Tool(
    name="TraderAgent",
    func=trade_stock,
    description="Use this to place trades like 'buy 5 AAPL' or 'sell 3 TSLA'."
)
