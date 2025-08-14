import os
import sys

import pytest

# Добавляем путь к src в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import find_person_transfers


# Тестовые данные
TEST_TRANSACTIONS = [
    # Подходящая транзакция (перевод физлицу)
    {"Категория": "Переводы", "Описание": "Перевод Ивану П.", "Сумма операции": -1000.0},
    # Не подходит - нет имени/фамилии
    {"Категория": "Переводы", "Описание": "Перевод между счетами", "Сумма операции": -500.0},
    # Не подходит - другая категория
    {"Категория": "Покупки", "Описание": "Петр В. Магазин", "Сумма операции": -200.0},
    # Подходит - русские буквы
    {"Категория": "Переводы", "Описание": "Анна С.", "Сумма операции": -1500.0},
    # Подходит - с дополнительным текстом
    {"Категория": "Переводы", "Описание": "Возврат долга Сергею М. за обед", "Сумма операции": -800.0},
]


def test_find_person_transfers_returns_list():
    """Тест, что функция возвращает список"""
    result = find_person_transfers([])
    assert isinstance(result, list)


def test_find_person_transfers_finds_correct_transfers():
    """Тест что функция правильно находит переводы физлицам"""
    result = find_person_transfers(TEST_TRANSACTIONS)

    assert len(result) == 3  # Должно найти 3 подходящих транзакции
    descriptions = [t["Описание"] for t in result]
    assert "Перевод Ивану П." in descriptions
    assert "Анна С." in descriptions
    assert "Возврат долга Сергею М. за обед" in descriptions


def test_find_person_transfers_ignores_non_transfers():
    """Тест, что функция игнорирует неподходящие транзакции"""
    result = find_person_transfers(TEST_TRANSACTIONS)

    descriptions = [t["Описание"] for t in result]
    assert "Перевод между счетами" not in descriptions
    assert "Петр В. Магазин" not in descriptions


def test_find_person_transfers_handles_invalid_data():
    """Тест обработки некорректных данных"""
    result = find_person_transfers(TEST_TRANSACTIONS)
    # Проверяем что строка была проигнорирована
    assert len(result) == 3


def test_find_person_transfers_empty_input():
    """Тест работы с пустым входом"""
    result = find_person_transfers([])
    assert len(result) == 0
    assert isinstance(result, list)


def test_find_person_transfers_with_none():
    """Тест работы с None входом"""
    with pytest.raises(TypeError):
        find_person_transfers(None)
