import json
import os
import sys
from unittest.mock import MagicMock, patch


# Добавляем путь к src в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_main_success():
    """Тест успешного выполнения main()"""
    with patch('src.views.get_transactions_for_month_period') as mock_trans, \
            patch('src.views.generate_report') as mock_report, \
            patch('src.views.get_currency_rates') as mock_curr, \
            patch('src.views.get_stock_price') as mock_stock, \
            patch('builtins.open') as mock_open:
        test_transactions = [{
            "Дата операции": "01.04.2023 12:00",
            "Номер карты": "1234567890123456",
            "Сумма операции": "-1000.00",
            "Бонусы (включая кэшбэк)": "10.00",
            "Категория": "Супермаркет",
            "Описание": "Покупки"
        }]

        mock_trans.return_value = test_transactions
        mock_report.return_value = {
            "greeting": "Тест",
            "cards": [],
            "top_transactions": []
        }
        mock_curr.return_value = {"USD": 75.0}
        mock_stock.return_value = {"AAPL": 150.0}
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        from src.views import main
        result = main("01.04.2023")

        # Преобразуем результат в dict для удобства проверки
        result_data = json.loads(result)

        # Проверяем результат
        assert result_data["greeting"] == "Тест"
        assert result_data["currency_rates"]["USD"] == 75.0
        assert result_data["stock_prices"]["AAPL"] == 150.0

        # Проверяем вызовы
        mock_trans.assert_called_once()
        mock_report.assert_called_once_with(test_transactions)
        mock_curr.assert_called_once()
        mock_stock.assert_called_once()
