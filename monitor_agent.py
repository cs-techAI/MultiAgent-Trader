# agents/monitor_agent.py

from langchain.tools import Tool
from services.memory_service import MemoryService
from services.portfolio_service import PortfolioService


# for monitoring the portfolio
memory = MemoryService()

def monitor_portfolio(user_input: str) -> str:
    memory.log_user_input(user_input)

    # Memory
    user_history = memory.get_user_history()
    trade_history = memory.get_trade_history()

    user_section = "\n".join([f"- [{ts}] {text}" for ts, text in user_history])
    trade_section = "\n".join([f"- [{ts}] {action} {qty} of {asset} → {result}" for ts, action, asset, qty, result in trade_history])





    # Real Portfolio Data
    positions = PortfolioService.get_positions()
    holdings = []
    if isinstance(positions, list) and positions:
        for p in positions:
            holdings.append(f"- {p['symbol']}: {p['qty']} shares @ ${p['avg_entry_price']}")
    holdings_section = "\n".join(holdings) if holdings else "No open positions found."



    # Open Orders
    orders = PortfolioService.get_open_orders()
    open_orders = []
    if isinstance(orders, list) and orders:
        for o in orders:
            open_orders.append(f"- {o['side']} {o['qty']} {o['symbol']} → {o['status']}")
    orders_section = "\n".join(open_orders) if open_orders else "No pending orders."


    return f"""📊 Portfolio Monitor Summary:

🧠 Recent User Questions:
{user_section or "No user questions yet."}

💼 Recent Trades:
{trade_section or "No trades logged yet."}

📦 Current Holdings:
{holdings_section}

⏳ Pending Orders:
{orders_section}
"""



monitor_agent = Tool(
    name="MonitorAgent",
    func=monitor_portfolio,
    description="Use this to report portfolio, trade history, user memory, and open orders."
)
