import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from typing import List, Dict
import pandas as pd
from src.utils import (
    get_greeting,
    read_xlsx_file,
    get_transactions_for_month_period,
    generate_report,
    XLSX_PATH,
    logger
)

# Параметризованный тест для всех временных диапазонов
@pytest.mark.parametrize("hour,expected", [
    (4, "Доброй ночи"),
    (5, "Доброе утро"),
    (11, "Доброе утро"),
    (12, "Добрый день"),
    (16, "Добрый день"),
    (17, "Добрый вечер"),
    (22, "Добрый вечер"),
    (23, "Доброй ночи"),
])
def test_get_greeting_time_ranges(hour, expected):
    test_time = datetime(2023, 1, 1, hour)
    assert get_greeting(test_time) == expected

# Тест для None (должен использовать текущее время)
@patch('src.utils.datetime')
def test_get_greeting_none_input(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 10)  # 10:00 - утро
    assert get_greeting(None) == "Доброе утро"


# Тест успешного чтения файла
@patch('pandas.read_excel')
def test_read_xlsx_success(mock_read):
    # Подготовка тестовых данных
    test_data = [{"Дата": "01.01.2023", "Сумма": 100}]
    mock_df = MagicMock()
    mock_df.to_dict.return_value = test_data
    mock_read.return_value = mock_df

    # Вызов и проверка
    result = read_xlsx_file("test.xlsx")
    assert result == test_data


# Тест ошибки при чтении файла
@patch('pandas.read_excel')
def test_read_xlsx_failure(mock_read):
    mock_read.side_effect = Exception("Ошибка чтения")

    result = read_xlsx_file("bad_file.xlsx")
    assert result == []


# Тестовые данные
@pytest.fixture
def sample_transactions():
    return [
        {"Дата операции": "01.04.2023 12:00", "Сумма": 100},
        {"Дата операции": "15.04.2023 18:30", "Сумма": 200},
        {"Дата операции": "30.03.2023 09:15", "Сумма": 300},
    ]

# Тест успешной фильтрации
def test_filter_transactions(sample_transactions):
    result = get_transactions_for_month_period("20.04.2023", sample_transactions)
    assert len(result) == 2  # Должны вернуться 2 транзакции за апрель
    assert all("04.2023" in t["Дата операции"] for t in result)

# Тест неверного формата даты
def test_invalid_date_format(sample_transactions):
    with patch('src.utils.logger.error') as mock_logger:
        result = get_transactions_for_month_period("2023-04-20", sample_transactions)
        assert result == []
        mock_logger.assert_called_once()

# Тест пустого списка транзакций
def test_empty_transactions():
    result = get_transactions_for_month_period("20.04.2023", [])
    assert result == []


# Фикстура с тестовыми транзакциями
@pytest.fixture
def sample_transactions():
    return [
        {
            "Номер карты": "1234567890123456",
            "Сумма операции": "-1000.50",
            "Бонусы (включая кэшбэк)": "10.05",
            "Дата операции": "01.04.2023 12:00",
            "Категория": "Супермаркет",
            "Описание": "Покупки"
        },
        {
            "Номер карты": "1234567890123456",
            "Сумма операции": "-500.75",
            "Бонусы (включая кэшбэк)": "5.00",
            "Дата операции": "15.04.2023 18:30",
            "Категория": "Кафе",
            "Описание": "Обед"
        }
    ]


# Тест генерации отчета
@patch('src.utils.get_greeting')
def test_generate_report(mock_greeting, sample_transactions):
    mock_greeting.return_value = "Добрый день"

    report = generate_report(sample_transactions)

    # Проверяем структуру отчета
    assert "greeting" in report
    assert "cards" in report
    assert "top_transactions" in report

    # Проверяем данные по картам
    assert len(report["cards"]) == 1
    card = report["cards"][0]
    assert card["last_digits"] == "3456"
    assert card["total_spent"] == 1501.25
    assert card["cashback"] == 15.05

    # Проверяем топ транзакций
    assert len(report["top_transactions"]) == 2
    assert report["top_transactions"][0]["amount"] == -1000.50
    assert report["top_transactions"][1]["category"] == "Кафе"


# Тест с пустым списком транзакций
@patch('src.utils.get_greeting')
def test_empty_transactions(mock_greeting):
    mock_greeting.return_value = "Добрый день"

    report = generate_report([])

    assert report["cards"] == []
    assert report["top_transactions"] == []
