# services/alpaca_service.py

import requests
from dotenv import load_dotenv
load_dotenv()

class AlpacaService:
    BASE_URL = "https://paper-api.alpaca.markets"

    @staticmethod
    def place_order(api_key, secret_key, symbol: str, qty: int, side: str, type: str = "market", time_in_force: str = "gtc"):
        url = f"{AlpacaService.BASE_URL}/v2/orders"
        headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key,
            "Content-Type": "application/json"
        }
        payload = {
            "symbol": symbol.upper(),
            "qty": qty,
            "side": side.lower(),
            "type": type,
            "time_in_force": time_in_force
        }

        try:
            print("📤 Placing Alpaca Order...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print("✅ Alpaca Order Response:", response.json())
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                error_message = response.json().get("message", str(http_err))
            except:
                error_message = str(http_err)
            print("❌ Alpaca HTTP Error:", error_message)
            return {"error": error_message}
        except Exception as e:
            print("❌ Unexpected Alpaca Error:", str(e))
            return {"error": str(e)}
