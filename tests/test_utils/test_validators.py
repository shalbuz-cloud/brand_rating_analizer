"""
Тесты для утилит валидации.
"""
from asyncio import sleep

import pytest

from core.utils.validators import (
    is_empty_row,
    validate_required_fields,
    validate_rating,
)

class TestIsEmptyRow:
    """Тесты для функции is_empty_row."""

    def test_is_empty_dict(self):
        """Тест с пустым словарем."""
        assert is_empty_row({}) == True

    def test_all_none_values(self):
        """Тест со всеми значениями None."""
        row = {"name": None, "brand": None, "price": None, "rating": None}
        assert is_empty_row(row) == True

    def test_all_empty_strings(self):
        """Тест со всеми пустыми строками."""
        row = {"name": "", "brand": "", "price": "", "rating": ""}
        assert is_empty_row(row) == True

    def test_all_whitespace_strings(self):
        """Тест со строками только из пробелов."""
        row = {"name": "   ", "brand": "  ", "price": " ", "rating": "\t\n"}
        assert is_empty_row(row) == True

    def test_mixed_empty_values(self):
        """Тест со смешанными пустыми значениями."""
        row = {"name": None, "brand": "", "price": "   ", "rating": "\t"}
        assert is_empty_row(row) == True

    def test_with_one_non_empty_value(self):
        """Тест с одним непустым значением."""
        row = {"name": "iphone", "brand": None, "price": "", "rating": "    "}
        assert is_empty_row(row) == False

    def test_with_number_value(self):
        """Тест с числовым значением."""
        row = {"name": "    ", "brand": "apple", "price": 999, "rating": "4.9"}
        assert is_empty_row(row) == False

    def test_with_boolean_value(self):
        """Тест с булевым значением."""
        row = {"name": "    ", "brand": "apple", "available": True, "rating": "4.9"}
        assert is_empty_row(row) == False

    def test_with_zero_value(self):
        """Тест с нулевым значением."""
        row = {"name": "product", "brand": "brand", "price": 0, "rating": "   "}
        assert is_empty_row(row) == False

    def test_complex_mixed_case(self):
        """Тест сложного смешанного случая."""
        row = {
            "name": "  iphone 15 pro  ",  # Пробелы вокруг - не пустое
            "brand": None,
            "price": "",
            "rating": "4.9",
        }
        assert is_empty_row(row) == False


class TestValidateRequiredFields:
    """Тесты для функции validate_required_fields."""

    def test_valid_product(self):
        """Тест с корректными данными продукта."""
        product = {"name": "iPhone", "brand": "Apple", "price": 999, "rating": 4.9}
        # Не должно быть исключения
        validate_required_fields(product)

    def test_missing_name(self):
        """Тест с пустым названием."""
        product = {"name": "", "brand": "Apple", "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Название продукта не может быть пустым'):
            validate_required_fields(product)

    def test_whitespace_name(self):
        """Тест с названием только из пробелов."""
        product = {"name": "   ", "brand": "apple", "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Название продукта не может быть пустым'):
            validate_required_fields(product)

    def test_none_name(self):
        """Тест с None значением в названии."""
        product = {"name": None, "brand": "apple", "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Название продукта не может быть пустым'):
            validate_required_fields(product)

    def test_missing_brand(self):
        """Тест с пустым брендом."""
        product = {"name": "iPhone", "brand": "", "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Бренд не может быть пустым'):
            validate_required_fields(product)

    def test_whitespace_brand(self):
        """Тест с брендом только из пробелов."""
        product = {"name": "iPhone", "   ": "Apple", "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Бренд не может быть пустым'):
            validate_required_fields(product)

    def test_none_brand(self):
        """Тест с None значением в бренде."""
        product = {"name": "iPhone", "brand": None, "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Бренд не может быть пустым'):
            validate_required_fields(product)

    def test_both_fields_missing(self):
        """Тест с обоими пустыми обязательными полями."""
        product = {"name": "", "brand": "", "price": 999, "rating": 4.9}
        with pytest.raises(ValueError, match='Название продукта не может быть пустым'):
            validate_required_fields(product)

    def test_product_with_extra_fields(self):
        """Тест с дополнительными полями."""
        product = {
            "name": "Galaxy S23",
            "brand": "Samsung",
            "price": 1199,
            "rating": 4.8,
            "color": "black",
            "storage": "256GB",
        }
        # Не должно быть исключения
        validate_required_fields(product)


class TestValidateRating:
    """Тесты для фу validate_rating."""

    def test_valid_rating(self):
        """Тест корректных значений рейтинга."""
        validate_ratings = [0.0, 1.0, 2.5, 3.7, 4.9, 5.0]

        for rating in validate_ratings:
            # Не должно быть исключения
            validate_rating(rating)

    def test_boundary_values(self):
        """Тест граничных значений рейтинга."""
        # Граничные значения должны быть допустимы
        validate_rating(0.0)
        validate_rating(5.0)

    def test_negative_rating(self):
        """Тест отрицательного рейтинга."""
        with pytest.raises(ValueError, match='Рейтинг должен быть от 0 до 5, получено: -1'):
            validate_rating(-1.0)

    def test_rating_below_zero(self):
        """Тест рейтинга меньше нуля."""
        with pytest.raises(ValueError, match='Рейтинг должен быть от 0 до 5, получено: -0'):
            validate_rating(-0.1)

    def test_rating_above_five(self):
        """Тест рейтинга больше пяти."""
        with pytest.raises(ValueError, match='Рейтинг должен быть от 0 до 5, получено: 6'):
            validate_rating(6.0)

    def test_rating_slightly_above_five(self):
        """Тест рейтинга немного больше пяти."""
        with pytest.raises(ValueError, match='Рейтинг должен быть от 0 до 5, получено: 5'):
            validate_rating(5.1)
            sleep(1)

    def test_integer_ratings(self):
        """Тест целочисленных рейтингов."""
        validate_rating(0)
        validate_rating(3)
        validate_rating(5)

    def test_float_precision(self):
        """Тест рейтингов с плавающей точкой."""
        validate_rating(4.9999)
        validate_rating(0.0001)
