import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


# Добавляем путь к src в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import main


@pytest.fixture
def mock_dependencies():
    with patch("src.main.get_transactions_for_month_period") as mock_transactions, patch(
        "src.main.find_person_transfers"
    ) as mock_find_transfers, patch("src.main.spending_by_category") as mock_spending, patch(
        "src.main.generate_report"
    ) as mock_report, patch(
        "src.main.get_currency_rates"
    ) as mock_rates, patch(
        "src.main.get_stock_price"
    ) as mock_stocks:
        # Настраиваем реалистичные моки
        mock_transactions.return_value = [
            {"Дата операции": "20.05.2018 12:00:00", "Категория": "Супермаркеты", "Сумма операции": -100.0},
            {
                "Дата операции": "21.05.2018 13:00:00",
                "Категория": "Переводы",
                "Описание": "Иван П.",
                "Сумма операции": -500.0,
            },
        ]

        mock_find_transfers.return_value = [
            {
                "Дата операции": "21.05.2018 13:00:00",
                "Категория": "Переводы",
                "Описание": "Иван П.",
                "Сумма операции": -500.0,
            }
        ]

        # Создаем реалистичный DataFrame для spending_by_category
        spending_data = {
            "Дата операции": ["20.05.2018 12:00:00"],
            "Категория": ["Супермаркеты"],
            "Сумма операции": [-100.0],
            "Описание": ["Покупка продуктов"],
        }
        mock_df = pd.DataFrame(spending_data)
        mock_spending.return_value = mock_df

        # Настраиваем полный отчет
        mock_report.return_value = {"greeting": "Добрый день", "cards": [], "top_transactions": []}

        mock_rates.return_value = [{"currency": "USD", "rate": 75.5}]
        mock_stocks.return_value = {"AAPL": 150.0}

        yield


def test_main_success(mock_dependencies):
    """Тест успешного выполнения"""
    result = main("20.05.2018")
    report = json.loads(result)

    assert isinstance(report, dict)
    assert "greeting" in report
    assert "person_transfers" in report
    assert "spending_analysis" in report
    assert "currency_rates" in report
    assert "stock_prices" in report


def test_main_error_handling():
    """Тест обработки ошибок"""
    with patch("src.main.get_transactions_for_month_period", side_effect=Exception("Test error")):
        result = main("20.05.2018")
        error_report = json.loads(result)
        assert "error" in error_report
        assert error_report["error"] == "Test error"


def test_main_output_structure(mock_dependencies):
    """Тест структуры отчета"""
    result = main("20.05.2018")
    report = json.loads(result)

    assert isinstance(report["person_transfers"], list)
    assert "category" in report["spending_analysis"]
    assert "transactions" in report["spending_analysis"]
    assert "total_spent" in report["spending_analysis"]


def test_main_with_invalid_date():
    """Тест с невалидной датой"""
    result = main("invalid-date")
    assert "error" in json.loads(result)


def test_main_file_creation(mock_dependencies):
    """Тест создания файла"""
    with patch("builtins.open", MagicMock()) as mock_open:
        main("20.05.2018")
        mock_open.assert_called_once_with("output.json", "w", encoding="utf-8")
