import json
import logging
import re


logger = logging.getLogger(__name__)


def find_person_transfers(transactions):
    """
    Находит переводы физическим лицам.
    Транзакция считается переводом физлицу, если:
    - Категория = "Переводы"
    - В описании есть имя и первая буква фамилии с точкой (например, "Валерий А.")
    """
    pattern = re.compile(r'[А-Яа-яёЁ]+\s[А-Яа-яёЁ]\.')
    person_transfers = []

    for transaction in transactions:
        try:
            # Если transaction — строка, пропускаем её
            if isinstance(transaction, str):
                logger.warning(f"Пропущена строка: {transaction}")
                continue

            category = transaction.get('Категория', '')
            description = transaction.get('Описание', '')

            if category == 'Переводы' and pattern.search(description):
                person_transfers.append(transaction)
                logger.info(f"Найден перевод физлицу: {description}")

        except Exception as e:
            logger.error(f"Ошибка при обработке транзакции: {e}")

    return person_transfers

    # return json.dumps(person_transfers, ensure_ascii=False, indent=4)
