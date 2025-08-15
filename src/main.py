import json
import logging
from datetime import datetime

import pandas as pd

from api_data import get_currency_rates, get_stock_price
from services import find_person_transfers
from src.reports import spending_by_category
from utils import generate_report, get_transactions_for_month_period, xlsx_transactions


# Настройка логирования
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
# Логгер для текущего модуля
logger = logging.getLogger(__name__)


def main(date: str):
    """Главная функция"""
    try:
        transactions = get_transactions_for_month_period(date, xlsx_transactions)

        # Конвертируем в DataFrame для анализа
        df_transactions = pd.DataFrame(transactions)

        # Преобразуем Timestamp в строку для всех datetime колонок
        datetime_cols = df_transactions.select_dtypes(include=["datetime64"]).columns
        for col in datetime_cols:
            df_transactions[col] = df_transactions[col].dt.strftime("%d.%m.%Y %H:%M:%S")

        # Вызываем поиск переводов ДО генерации отчета
        person_transfers = find_person_transfers(df_transactions.to_dict("records"))

        # Анализ трат по категориям
        target_category = "Супермаркеты"
        category_spending = spending_by_category(df_transactions, target_category, date)

        # Генерируем отчёт
        report = generate_report(transactions)
        # print(report)
        report.update(
            {
                "person_transfers": person_transfers,
                "spending_analysis": {
                    "category": target_category,
                    "transactions": category_spending.to_dict("records"),
                    "total_spent": category_spending["Сумма операции"].sum(),
                },
                "currency_rates": get_currency_rates(),
                "stock_prices": get_stock_price(),
            }
        )

        # Сериализуем в JSON с обработкой специальных типов
        def json_serializer(obj):
            if pd.isna(obj):
                return None
            if isinstance(obj, (pd.Timestamp, datetime)):
                return obj.strftime("%d.%m.%Y %H:%M:%S")
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        json_output = json.dumps(report, ensure_ascii=False, indent=4, default=json_serializer)
        #       json_output = json.dumps(report, ensure_ascii=False, indent=4)
        with open("output.json", "w", encoding="utf-8") as f:
            f.write(json_output)
        return json_output
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)

        # Получаем данные
        stock_prices = get_stock_price()
        currency_rates = get_currency_rates()

        # Добавляем курсы валют и акций в отчёт
        report.update({"currency_rates": currency_rates, "stock_prices": stock_prices})

        # Возвращаем результат
        json_output = json.dumps(report, ensure_ascii=False, indent=4)

        # Сохраняем в файл
        with open("output.json", "w", encoding="utf-8") as f:
            f.write(json_output)

            return json_output

    except Exception as e:
        logger.error(f"Ошибка в main(): {e}")
        error_msg = {"error": str(e)}
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(error_msg, f)
        return json.dumps(error_msg, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(main("20.05.2018"))
