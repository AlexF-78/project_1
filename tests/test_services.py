# import pytest
import json
import os
import sys


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


def test_find_person_transfers_returns_json():
    """Тест, что функция возвращает валидный JSON"""
    result = find_person_transfers([])
    assert isinstance(result, str)
    json.loads(result)  # не должно вызывать исключение


def test_find_person_transfers_finds_correct_transfers():
    """Тест что функция правильно находит переводы физлицам"""
    result = json.loads(find_person_transfers(TEST_TRANSACTIONS))

    assert len(result) == 3  # Должно найти 3 подходящих транзакции
    descriptions = [t["Описание"] for t in result]
    assert "Перевод Ивану П." in descriptions
    assert "Анна С." in descriptions
    assert "Возврат долга Сергею М. за обед" in descriptions


def test_find_person_transfers_ignores_non_transfers():
    """Тест, что функция игнорирует неподходящие транзакции"""
    result = json.loads(find_person_transfers(TEST_TRANSACTIONS))

    descriptions = [t["Описание"] for t in result]
    assert "Перевод между счетами" not in descriptions
    assert "Петр В. Магазин" not in descriptions


def test_find_person_transfers_empty_input():
    """Тест работы с пустым входом"""
    result = json.loads(find_person_transfers([]))
    assert len(result) == 0
