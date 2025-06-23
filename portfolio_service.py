# services/portfolio_service.py

import requests
from dotenv import load_dotenv
load_dotenv()

class PortfolioService:
    BASE_URL = "https://paper-api.alpaca.markets"

    @staticmethod
    def get_positions(api_key, secret_key):
        url = f"{PortfolioService.BASE_URL}/v2/positions"
        headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_open_orders(api_key, secret_key):
        url = f"{PortfolioService.BASE_URL}/v2/orders"
        headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }
        try:
            response = requests.get(url, headers=headers, params={"status": "open"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
