"""
Утилиты для валидации данных.
"""

from typing import Any


class DataValidator:
    """Валидатор данных продуктов."""

    @staticmethod
    def is_empty_row(row: dict[str, Any]) -> bool:
        """
        Проверяет, является ли строка пустой.
        Строка считается пустой, если все значения None, пустые строки или строки только из пробелов.

        :param row: Словарь с данными строки

        :return: True - если строка пустая, иначе - False
        """
        if not row:
            return True

        for value in row.values():
            if value is not None and str(value).strip():
                return False

        return True

    @staticmethod
    def validate_required_fields(product_data: dict[str, Any]) -> None:
        """
        Проверяет, что все обязательные поля заполнены.

        :param product_data: Словарь с данными продукта

        :raise ValueError: Если какое-либо обязательное поле пустое
        """
        name = product_data.get("name")
        brand = product_data.get("brand")

        if not name or (isinstance(name, str) and not name.strip()):
            raise ValueError("Product name cannot be empty")
        if not brand or (isinstance(brand, str) and not brand.strip()):
            raise ValueError("Brand cannot be empty")

    @staticmethod
    def validate_rating(rating: float) -> None:
        """
        Проверяет корректность рейтинга.

        :param rating: Рейтинг для проверки

        :raise ValueError: Если рейтинг не в диапазоне от 0 до 5
        """
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5, got %.2f" % rating)
