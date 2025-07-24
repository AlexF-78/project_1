# tests/test_api_data.py
import pytest
from unittest.mock import patch, MagicMock
from src.api_data import get_stock_price, get_currency_rates


# Тесты для get_stock_price()
@patch('requests.get')
def test_get_stock_price_success(mock_get):
    """Тест успешного получения цен акций"""
    # Настраиваем mock ответа
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Global Quote": {
            "05. price": "150.50"
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch('src.api_data.STOCKS', ['AAPL']), \
            patch('src.api_data.STOCK_API_KEY', 'test_key'):
        result = get_stock_price()
        assert result == {'AAPL': 150.5}
        mock_get.assert_called_once()


@patch('requests.get')
def test_get_stock_price_failure(mock_get):
    """Тест ошибки при получении цен"""
    mock_get.side_effect = Exception("API Error")

    with patch('src.api_data.STOCKS', ['AAPL']):
        result = get_stock_price()
        assert result == {'AAPL': 0.0}


# Тесты для get_currency_rates()
@patch('requests.get')
def test_get_currency_rates_success(mock_get):
    """Тест успешного получения курсов валют"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Valute": {
            "USD": {"Value": 75.50},
            "EUR": {"Value": 85.25}
        }
    }
    mock_get.return_value = mock_response

    result = get_currency_rates()
    assert result == [
        {"currency": "USD", "rate": 75.50},
        {"currency": "EUR", "rate": 85.25}
    ]


@patch('requests.get')
def test_get_currency_rates_fallback(mock_get):
    """Тест возврата резервных значений при ошибке"""
    mock_get.side_effect = Exception("API Error")

    result = get_currency_rates()
    assert result == [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]


# Параметризованный тест для проверки разных символов
@pytest.mark.parametrize("symbol", ["AAPL", "GOOGL", "TSLA"])
@patch('requests.get')
def test_get_stock_price_different_symbols(mock_get, symbol):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Global Quote": {
            "05. price": "100.00"
        }
    }
    mock_get.return_value = mock_response

    with patch('src.api_data.STOCKS', [symbol]):
        result = get_stock_price()
        assert result == {symbol: 100.0}