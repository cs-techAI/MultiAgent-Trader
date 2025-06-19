# services/news_service.py

import os
import requests
from dotenv import load_dotenv


load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# fetches latest market news using finnhub api key

class NewsService:
    
    @staticmethod
    def get_market_news():
        url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
        try:


            response = requests.get(url)
            response.raise_for_status()
            return response.json()[:5]  # top 5 headlines
        


        except Exception as e:
            return [{"headline": f"Failed to load news: {e}"}]
