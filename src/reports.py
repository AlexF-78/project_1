# import json
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца от указанной даты.

    Args:
        transactions: DataFrame с транзакциями
        category: Название категории для анализа
        date: Опциональная дата в формате 'dd.mm.YYYY'. Если None - используется текущая дата.

    Returns:
        DataFrame с отфильтрованными транзакциями
    """
    logger = logging.getLogger(__name__)

    try:
        # Преобразуем дату или берем текущую
        if date:
            end_date = datetime.strptime(date, "%d.%m.%Y")
        else:
            end_date = datetime.now()

        # Вычисляем дату начала периода (3 месяца назад)
        start_date = end_date - relativedelta(months=3)

        logger.info(f"Анализ трат по категории '{category}' с {start_date.date()} по {end_date.date()}")

        # Преобразуем даты операций в datetime
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        # Фильтруем по категории и дате
        filtered = transactions[
            (transactions["Категория"] == category)
            & (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
        ]

        # Отбираем только отрицательные суммы (траты)
        filtered = filtered[filtered["Сумма операции"] < 0]

        logger.info(f"Найдено {len(filtered)} транзакций по категории '{category}'")

        return filtered

    except Exception as e:
        logger.error(f"Ошибка при анализе трат по категории: {e}")
        raise
