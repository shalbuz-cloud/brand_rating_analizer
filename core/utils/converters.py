"""
Утилиты для преобразования данных.
"""

from typing import Any


def safe_strip(value: Any) -> str:
    """
    Безопасно применяет strip() к значению, обрабатывая None и не строковые значения.

    :param value: Значение для обработки

    :return: Очищенная строка или пустая строка, если значение None
    """
    if value is None:
        return ""

    # Преобразуем в строку, если это не строка
    if not isinstance(value, str):
        value = str(value)

    return value.strip()


def safe_float(value: Any) -> float:
    """
    Безопасно преобразует значение в float, обрабатывая None и некорректные значения.

    :param value: Значение для преобразования

    :return: Число с плавающей точкой

    :raise ValueError: Если значение не может быть преобразовано в число
    """
    if value is None:
        raise ValueError('Значение не может быть None')

    # Если это строка, очищаем ее
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            raise ValueError('Значение не может быть пустой строкой')

    try:
        return float(value)
    except (ValueError, TypeError) as e:
        raise ValueError('Невозможно преобразовать %s в число: %s' % (value, e))
