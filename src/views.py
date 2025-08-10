import json
import logging

from api_data import get_currency_rates, get_stock_price
from utils import (  # get_greeting,; read_xlsx_file,
    generate_report,
    get_transactions_for_month_period,
    xlsx_transactions,
)


# Настройка логирования ДО всех других операций
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # Запись в файл
        logging.FileHandler("app.log"),
        # Вывод в консоль (опционально)
        logging.StreamHandler(),
    ],
)
# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)


def main(date: str):
    """Главная функция"""
    transactions = get_transactions_for_month_period(date, xlsx_transactions)

    # Генерируем отчёт
    report = generate_report(transactions)
    # print(report)

    # Получаем данные
    stock_prices = get_stock_price()
    currency_rates = get_currency_rates()

    # Добавляем курсы валют и акций в отчёт
    report.update({"currency_rates": currency_rates, "stock_prices": stock_prices})

    # Сериализуем в JSON
    json_output = json.dumps(report, ensure_ascii=False, indent=4)

    # Сохраняем в файл
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(json_output)

    return json.dumps(report, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(main("27.07.2019"))
