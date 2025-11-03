"""
Тесты для модуля вычисления статистик.
"""

import pytest
from core.calculator import calculate_brand_ratings


class TestCalculatorBrandRatings:
    """Тесты для функции calculate_brand_ratings."""

    def test_basic_calculation(self):
        """Тест базового расчета рейтингов."""
        products = [
            {"brand": "apple", "rating": 4.9},
            {"brand": "apple", "rating": 4.7},
            {"brand": "samsung", "rating": 4.8},
            {"brand": "samsung", "rating": 4.6},
        ]

        result = calculate_brand_ratings(products)

        assert len(result) == 2
        apple_data = next(item for item in result if item['brand'] == "apple")
        samsung_data = next(item for item in result if item['brand'] == "samsung")

        assert apple_data['average_rating'] == 4.8  # (4.9 + 4.7) / 2
        assert samsung_data['average_rating'] == 4.7  # (4.8 + 4.5) / 2
        assert apple_data['product_count'] == 2
        assert samsung_data['product_count'] == 2

    def test_single_product_per_brand(self):
        """Тест с одним продуктом на бренд."""
        products = [
            {"brand": "apple", "rating": 4.9},
            {"brand": "samsung", "rating": 4.8},
            {"brand": "xiaomi", "rating": 4.6},
        ]

        result = calculate_brand_ratings(products)

        assert len(result) == 3
        assert result[0]['brand'] == 'apple'
        assert result[0]['average_rating'] == 4.9
        assert result[0]['product_count'] == 1

    def test_sorting_order(self):
        """Тест правильности сортировки по рейтингу."""
        products = [
            {"brand": "low", "rating": 3.0},
            {"brand": "high", "rating": 5.0},
            {"brand": "medium", "rating": 4.0},
        ]

        result = calculate_brand_ratings(products)

        # Проверяем сортировку по убыванию рейтинга
        assert result[0]['brand'] == "high"
        assert result[0]['average_rating'] == 5.0
        assert result[1]['brand'] == "medium"
        assert result[1]['average_rating'] == 4.0
        assert result[2]['brand'] == "low"
        assert result[2]['average_rating'] == 3.0

    def test_case_insensitive_brands(self):
        """Тест обработки брендов в разных регистрах."""
        products = [
            {"brand": "Apple", "rating": 4.9},
            {"brand": "APPLE", "rating": 4.8},
            {"brand": "apple", "rating": 4.7},
        ]

        result = calculate_brand_ratings(products)

        # Все варианты должны быть объединены
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'
        assert result[0]['average_rating'] == pytest.approx(4.8)  # (4.9 + 4.8 + 4.7) / 3
        assert result[0]['product_count'] == 3

    def test_rounding_precision(self):
        """Тест округления до двух знаков после запятой."""
        products = [
            {"brand": "test", "rating": 4.666},
            {"brand": "test", "rating": 4.777},
        ]

        result = calculate_brand_ratings(products)

        assert result[0]['average_rating'] == 4.72  # (4.666 + 4.777) / 2 = 4.7215 -> 4.72

    def test_empty_product_list(self):
        """Тест с пустым списком продуктов."""
        result = calculate_brand_ratings([])

        assert result == []

    def test_single_brand_multiple_products(self):
        """Тест одного бренда с множеством продуктов."""
        products = [
            {"brand": "apple", "rating": 5.0},
            {"brand": "apple", "rating": 4.5},
            {"brand": "apple", "rating": 4.0},
            {"brand": "apple", "rating": 3.5},
            {"brand": "apple", "rating": 3.0},
        ]

        result = calculate_brand_ratings(products)

        assert len(result) == 1
        assert result[0]['brand'] == 'apple'
        assert result[0]['average_rating'] == 4.0  # (5 + 4.5 + 4 + 3.5 + 3) / 5 = 4.0
        assert result[0]['product_count'] == 5

    def test_zero_rating(self):
        """Тест с нулевым рейтингом."""
        products = [
            {"brand": "test", "rating": 0.0},
            {"brand": "test", "rating": 0.0},
        ]

        result = calculate_brand_ratings(products)

        assert result[0]['average_rating'] == 0.0
        assert result[0]['product_count'] == 2

    def test_very_small_ratings(self):
        """Тест с очень маленькими рейтингами."""
        products = [
            {"brand": "test", "rating": 0.001},
            {"brand": "test", "rating": 0.002},
        ]

        result = calculate_brand_ratings(products)

        assert result[0]['average_rating'] == 0.0  # 0.0015 округляется до 0.00

    def test_complex_mixed_scenario(self):
        """Тест сложного смешанного сценария."""
        products = [
            {"brand": "apple", "rating": 4.9, "price": 999},
            {"brand": "apple", "rating": 4.8, "price": 899},
            {"brand": "samsung", "rating": 4.7, "price": 799},
            {"brand": "xiaomi", "rating": 4.6, "price": 299},
            {"brand": "samsung", "rating": 4.5, "price": 699},
            {"brand": "xiaomi", "rating": 4.4, "price": 199},
            {"brand": "huawei", "rating": 4.3, "price": 499},
        ]

        result = calculate_brand_ratings(products)

        assert len(result) == 4

        # Проверяем правильность расчетов и сортировки
        brands = [item['brand'] for item in result]
        ratings = [item['average_rating'] for item in result]
        counts = [item['product_count'] for item in result]

        assert brands == ["apple", "samsung", "xiaomi", "huawei"]
        assert ratings == [4.85, 4.6, 4.5, 4.3]
        assert counts == [2, 2, 2, 1]
