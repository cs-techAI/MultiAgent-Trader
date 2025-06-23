# agents/analyzer_agent.py


from langchain.tools import Tool
from services.deepseek_service import DeepSeekService



def analyze_stock(query: str) -> str:
    
    # Extract symbol using DeepSeek
    symbol = DeepSeekService.extract_stock_symbol(query) or "this stock"


    prompt = f"""
You are a smart trading analyst. Analyze the following market query and provide an actionable recommendation.

Query: "{query}"

Respond in **3 structured markdown parts**:
1. **Summary**: What is the user's question really about?
2. **Market Insight**: Key trends, valuation, and risks related to the stock.
3. **Recommendation**: Should the user invest now? Short-term vs long-term advice.

At the end, include a follow-up question:
"Would you like to buy {symbol} stocks?"
"""

    return DeepSeekService.ask_deepseek(prompt)


analyzer_agent = Tool(
    name="AnalyzerAgent",
    func=analyze_stock,
    description="Use this to analyze a stock or market query and suggest whether to invest."
)
