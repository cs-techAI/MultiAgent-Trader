# services/deepseek_service.py

# for llm
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



class DeepSeekService:
    
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

    @staticmethod
    def ask_deepseek(prompt: str) -> str:
        try:
            response = DeepSeekService.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            return response.choices[0].message.content


        except Exception as e:
            return f"[DeepSeek Error]: {e}"
        



    @staticmethod
    def handle_investment_followup(context: str, user_reply: str) -> dict:
        prompt = f"""
You are a financial assistant helping the user decide whether to invest.

Context:
{context}

User replied: "{user_reply}"

Based on this, decide the next step in the flow and return only a JSON object.

Valid actions:
- ask_quantity
- ask_confirmation
- execute_trade
- cancel
- unclear

Respond in this JSON format:
{{
  "action": "<action>",
  "message": "<your follow-up response>",
  "symbol": "<symbol>",
  "quantity": 10   // optional
}}

Only return valid JSON and nothing else.
"""
        reply = DeepSeekService.ask_deepseek(prompt)
        try:
            return json.loads(reply)
        except:
            return {
                "action": "unclear",
                "message": "Sorry, I didn't catch that. Could you clarify?",
            }
        



    @staticmethod
    def extract_stock_symbol(user_input: str) -> str:
        prompt = f"""
Extract the stock ticker symbol (1–5 capital letters) the user is referring to in this message:

"{user_input}"

Respond with just the ticker symbol in uppercase. If not found, say "UNKNOWN".
"""
        response = DeepSeekService.ask_deepseek(prompt).strip().upper()
        return response if response != "UNKNOWN" else None

    



    @staticmethod
    def suggest_action_for_stock(symbol: str) -> str:
        prompt = f"""
A user is currently holding stock: {symbol}.
Based on current market sentiment and fundamentals, what is your trading suggestion?

Respond with:
- 📉 Sell — if stock is overvalued or near-term risk is high
- 🛑 Hold — if stock is stable and no major action needed
- 📈 Buy More — if stock is undervalued or strong momentum

Also include 1-line justification.
"""
        return DeepSeekService.ask_deepseek(prompt)


#endd
