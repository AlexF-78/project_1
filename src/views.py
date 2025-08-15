import json
import logging
import os
import sys
from datetime import datetime

import pandas as pd

from src.api_data import get_currency_rates, get_stock_price
from src.reports import spending_by_category
from src.services import find_person_transfers
from src.utils import generate_report, get_transactions_for_month_period, xlsx_transactions


sys.path.append(os.path.dirname(__file__))

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


def generate_full_report(date: str):
    """Главная функция"""
    try:
        # Преобразуем входную дату из формата YYYY-MM-DD HH:MM:SS в DD.MM.YYYY
        input_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        formatted_date = input_date.strftime("%d.%m.%Y")

        # Получение и обработка транзакций
        transactions = get_transactions_for_month_period(formatted_date, xlsx_transactions)
        df_transactions = pd.DataFrame(transactions)

        # Преобразование временных меток
        datetime_cols = df_transactions.select_dtypes(include=["datetime64"]).columns
        for col in datetime_cols:
            df_transactions[col] = df_transactions[col].dt.strftime("%d.%m.%Y")

        # Анализ данных
        person_transfers = find_person_transfers(df_transactions.to_dict("records"))
        target_category = "Супермаркеты"
        category_spending = spending_by_category(df_transactions, target_category, formatted_date)

        # Формирование отчета
        report = generate_report(transactions)
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

        # Сериализация в JSON
        def json_serializer(obj):
            if pd.isna(obj):
                return None
            if isinstance(obj, (pd.Timestamp, datetime)):
                return obj.strftime("%d.%m.%Y")
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        json_output = json.dumps(report, ensure_ascii=False, indent=4, default=json_serializer)

        # Сохранение в файл
        with open("output.json", "w", encoding="utf-8") as f:
            f.write(json_output)

        return json_output

    except ValueError as e:
        logger.error(f"Ошибка формата даты: {e}")
        raise ValueError("Неверный формат даты. Ожидается YYYY-MM-DD HH:MM:SS")
        logger.error(f"Ошибка при генерации отчета: {e}")
    except Exception as e:
        error_msg = {"error": str(e)}
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(error_msg, f)
        return json.dumps(error_msg, ensure_ascii=False, indent=4)
