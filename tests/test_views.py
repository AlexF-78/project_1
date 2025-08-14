import os
import sys
from unittest.mock import MagicMock, patch

import pytest


# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from src.utils import xlsx_transactions
from src.views import generate_full_report


@pytest.fixture
def sample_transaction():
    return {
        "Дата операции": "01.07.2023 12:00:00",
        "Номер карты": "1234",
        "Сумма операции": -100.00,
        "Категория": "Супермаркеты",
        "Описание": "Покупка",
    }


def test_basic_execution(sample_transaction):
    """Просто проверяем что функция выполняется без ошибок"""
    with patch("views.get_transactions_for_month_period") as mock_trans, patch("views.find_person_transfers"), patch(
        "src.views.spending_by_category"
    ) as mock_spending, patch("views.generate_report"), patch("views.get_currency_rates"), patch(
        "views.get_stock_price"
    ), patch(
        "builtins.open", MagicMock()
    ):
        # Настраиваем моки
        mock_trans.return_value = [sample_transaction]

        # Вызываем функцию с датой для теста
        result = generate_full_report("2023-07-01 00:00:00")
        # Основная проверка (что функция возвращает строку)
        assert isinstance(result, str)

        # Проверяем, что spending_by_category получила правильную дату
        # (формат DD.MM.YYYY)
        called_date = mock_spending.call_args[0][2]  # Третий аргумент
        assert called_date == "01.07.2023", f"Ожидался формат DD.MM.YYYY, получили {called_date}"


def test_empty_transactions():
    """Тест с пустым списком транзакций"""
    with patch("views.get_transactions_for_month_period", return_value=[]), patch("builtins.open", MagicMock()):
        result = generate_full_report("2023-07-01 00:00:00")
        assert isinstance(result, str)


def test_error_handling():
    """Тест обработки ошибок"""
    with patch("views.get_transactions_for_month_period", side_effect=Exception("Test error")), patch(
        "builtins.open", MagicMock()
    ):
        result = generate_full_report("2023-07-01 00:00:00")
        assert "error" in result.lower()
