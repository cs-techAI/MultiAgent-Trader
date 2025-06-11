# services/portfolio_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class PortfolioService:
    API_KEY = os.getenv("ALPACA_API_KEY")
    SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")



    @staticmethod
    def get_positions():
        url = f"{PortfolioService.BASE_URL}/v2/positions"
        headers = {
            "APCA-API-KEY-ID": PortfolioService.API_KEY,
            "APCA-API-SECRET-KEY": PortfolioService.SECRET_KEY
        }



        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
    
            return {"error": str(e)}



    @staticmethod
    def get_open_orders():
        url = f"{PortfolioService.BASE_URL}/v2/orders"
        headers = {
            "APCA-API-KEY-ID": PortfolioService.API_KEY,
            "APCA-API-SECRET-KEY": PortfolioService.SECRET_KEY
        }



        try:
            response = requests.get(url, headers=headers, params={"status": "open"})
            response.raise_for_status()
            return response.json()
        

        
        except Exception as e:
            return {"error": str(e)}
