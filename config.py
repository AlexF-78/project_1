import os
from pathlib import Path
from dotenv import load_dotenv

# Указываем правильный путь к .env
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')


load_dotenv()


class Settings:
    # API Keys
    EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "13efaghyEH1cPaWtvn1Vw7yXfA7OI0e7")
    STOCK_API_KEY = os.getenv("STOCK_API_KEY")
    EXCHANGE_RATE_URL = "https://api.exchangerate.host/latest?base=RUB"

    # Настройки
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    CURRENCIES = ["USD", "EUR"]  # Валюты для отслеживания
    STOCKS = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]  # Акции для отслеживания

# Получаем путь к папке project_1
base_dir = os.path.dirname(os.path.abspath(__file__))

# Создаём полный путь к файлу operations.xlsx
XLSX_PATH = os.path.join(base_dir, "data", "operations.xlsx")

settings = {
    "logging_level": "INFO"
}
