import os
from typing import Dict

import requests


STOCK_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "2ZP58APSEP6BGVAO")
STOCKS = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def get_stock_price() -> Dict[str, float]:
    """Получает текущую цену акции через Alpha Vantage API из списка STOCKS"""

    base_url = "https://www.alphavantage.co/query"
    prices = {}
    for symbol in STOCKS:
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": STOCK_API_KEY
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                prices[symbol] = float(data["Global Quote"]["05. price"])
            else:
                print(f"Ошибка формата для {symbol}")
                prices[symbol] = 0.0

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса для {symbol}: {e}")
            prices[symbol] = 0.0
        except Exception as e:
            print(f"Неожиданная ошибка для {symbol}: {e}")
            prices[symbol] = 0.0

    return prices


def get_currency_rates():
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        data = response.json()
        return [
            {"currency": "USD",
             "rate": round(float(data["Valute"]["USD"]["Value"]), 2)},
            {"currency": "EUR",
             "rate": round(float(data["Valute"]["EUR"]["Value"]), 2)}
        ]
    except Exception:
        return [{"currency": "USD", "rate": 73.21}, {"currency": "EUR", "rate": 87.08}]


rates = get_currency_rates()
# print(rates)
