# main.py
from agents.router_agent import RouterAgent

router = RouterAgent()
print("💬 SmartTrader CLI — type 'exit' to quit.\n")

while True:
    q = input("You: ")
    if q.lower() == "exit":
        break
    print("SmartTrader:", router.route(q))
