# agents/router_agent.py

import os

from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

from agents.analyzer_agent import analyzer_agent
from agents.trader_agent import trader_agent
from agents.monitor_agent import monitor_agent
from services.deepseek_service import DeepSeekService

# routes to the main three agents as per the intent 

load_dotenv()

class RouterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

        
        
        self.tools = [
            Tool(
                name=analyzer_agent.name,
                func=analyzer_agent.func,
                description="Use this only if the user is asking for stock analysis, market insight, or investment advice."
            ),
            Tool(
                name=trader_agent.name,
                func=trader_agent.func,
                description="Use this only if the user wants to place a trade, such as 'buy 5 AAPL' or 'sell 3 TSLA'."
            ),
            Tool(
                name=monitor_agent.name,
                func=monitor_agent.func,
                description="Use this only if the user wants to view portfolio, trade history, or recent activity."
            )
        ]


        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )




    def classify_intent(self, user_input: str) -> str:
        prompt = f"""
Classify the user's message into exactly one of the following categories:

- analyze → if the user is asking for market insight, investment advice, or analysis
- trade → if the user wants to buy or sell a stock or asset
- monitor → if the user wants to view their portfolio, recent trades, or performance

Respond with just one word: 'analyze', 'trade', or 'monitor'

User message:
\"{user_input}\"

Answer:
"""
        response = DeepSeekService.ask_deepseek(prompt).lower()
        if "trade" in response:
            return "TraderAgent"
        elif "monitor" in response:
            return "MonitorAgent"
        elif "analyze" in response:
            return "AnalyzerAgent"
        else:
            return "SmartTrader"  
        



    def route(self, user_input: str) -> tuple[str, str]:
        try:
            intent_label = self.classify_intent(user_input)  # just for display
            response = self.agent.run(user_input)            # LLM decides what tool to run
            return response, intent_label
        except Exception as e:
            return f"❌ Routing Error: {str(e)}", "RouterAgent"
