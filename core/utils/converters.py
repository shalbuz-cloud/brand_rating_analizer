"""
Утилиты для преобразования данных.
"""

from typing import Any


class DataConverter:
    """Конвертер данных продуктов."""

    @staticmethod
    def safe_strip(value: Any) -> str:
        """
        Безопасно применяет strip() к значению, обрабатывая None и не строковые значения.

        :param value: Значение для обработки

        :return: Очищенная строка или пустая строка, если значение None
        """
        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def safe_float(value: Any) -> float:
        """
        Безопасно преобразует значение в float, обрабатывая None и некорректные значения.

        :param value: Значение для преобразования

        :return: Число с плавающей точкой

        :raise ValueError: Если значение не может быть преобразовано в число
        """
        if value is None:
            raise ValueError("Value cannot be None")

        # Если это строка, очищаем ее
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                raise ValueError("Value cannot be empty string")

        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise ValueError("Cannot convert %s to number: %s" % (value, e)) from e
