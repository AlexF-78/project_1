import logging
from datetime import datetime
from typing import Dict, List
import pandas as pd
from config import XLSX_PATH

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие по времени суток"""
    if current_time is None:
        current_time = datetime.now()
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"
    # greeting = get_greeting(current_time)
    # print(greeting)



def read_xlsx_file(file_path: str = XLSX_PATH) -> List[Dict]:
    """ Считывает XLSX файл и возвращает список словарей"""
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении файла XLSX: {e}")
        return []

xlsx_transactions = read_xlsx_file(XLSX_PATH)
# print(xlsx_transactions)



def get_transactions_for_month_period(input_date: str, transactions: list[dict]) -> list[dict]:
    """
    Возвращает транзакции с начала месяца по указанную дату.
    """
    try:
        end_date = datetime.strptime(input_date, "%d.%m.%Y").date()
        first_day_of_month = end_date.replace(day=1)

        filtered = []
        for trans in transactions:
            # Получаем только дату из строки (игнорируем время)
            trans_date_str = trans["Дата операции"].split()[0]
            trans_date = datetime.strptime(trans_date_str, "%d.%m.%Y").date()

            if first_day_of_month <= trans_date <= end_date:
                filtered.append(trans)
        return filtered
    except ValueError as e:
        logger.error(f"Ошибка формата даты: {e}")
        return []


# result= get_transactions_for_month_period("20.04.2020",  xlsx_transactions)
# print(result)


def generate_report(transactions: List[Dict]) -> Dict:
    """Генерирует базовый отчет по транзакциям"""
    cards = {}
    for t in transactions:
        card_num = str(t.get("Номер карты", "0000"))[-4:]
        amount = abs(float(t.get("Сумма операции", 0)))
        cashback = float(t.get("Бонусы (включая кэшбэк)", 0))

        if card_num not in cards:
            cards[card_num] = {"last_digits": card_num, "total_spent": 0.0, "cashback": 0.0}
        cards[card_num]["total_spent"] += amount
        cards[card_num]["cashback"] += cashback

    # Округляем значения до 2 знаков после запятой
    for card in cards.values():
        card["total_spent"] = float(f"{card["total_spent"]:.2f}")
        card["cashback"] = float(f"{card["cashback"]:.2f}")

    top_trans = sorted(
        [t for t in transactions
         if t.get("Сумма операции") is not None and float(t["Сумма операции"]) < 0],
        key=lambda x: abs(float(x["Сумма операции"])),
        reverse=True
    )[:5]

    return {
        "greeting": get_greeting(datetime.now()),
        "cards": list(cards.values()),
        "top_transactions": [{
            "date": t["Дата операции"].split()[0],
            "amount": float(f"{float(t['Сумма операции']):.2f}"),
            "category": t.get("Категория", "Не указана"),
            "description": t.get("Описание", "")
        } for t in top_trans]
    }
