"""
Утилиты для валидации данных.
"""

from typing import Dict, Any


def is_empty_row(row: Dict[str, Any]) -> bool:
    """
    Проверяет, является ли строка пустой.
    Строка считается пустой, если все значения None, пустые строки или строки только из пробелов.

    :param row: Словарь с данными строки

    :return: True - если строка пустая, иначе - False
    """
    if not row:
        return True

    for value in row.values():
        # Если значение не None и после strip() не пустое - строка не пустая
        if value is not None and str(value).strip() != "":
            return False

    return True


def validate_required_fields(product: Dict[str, Any]) -> None:
    """
    Проверяет, что все обязательные поля заполнены.

    :param product: Словарь с данными продукта

    :raise ValueError: Если какое-либо обязательное поле пустое
    """
    name = product.get('name')
    brand = product.get('brand')

    # Проверяем, что поля не None и не пустые/пробельные
    if not name or (isinstance(name, str) and not name.strip()):
        raise ValueError('Название продукта не может быть пустым')
    if not brand or (isinstance(brand, str) and not brand.strip()):
        raise ValueError('Бренд не может быть пустым')


def validate_rating(rating: float) -> None:
    """
    Проверяет корректность рейтинга.

    :param rating: Рейтинг для проверки

    :raise ValueError: Если рейтинг не в диапазоне от 0 до 5
    """
    if not 0 <= rating <= 5:
        raise ValueError('Рейтинг должен быть от 0 до 5, получено: %.2f' % rating)
