import pytest

from core.calculator import BrandRatingCalculator
from core.models import Product


@pytest.fixture
def calculator() -> BrandRatingCalculator:
    return BrandRatingCalculator()


class TestBrandRatingCalculator:
    """Тесты калькулятора рейтингов."""

    @pytest.mark.parametrize(
        "products,expected_count,expected_ratings",
        [
            (
                [
                    Product("iPhone", "apple", 999, 4.9),
                    Product("Galaxy", "samsung", 899, 4.8),
                ],
                2,
                {"apple": 4.9, "samsung": 4.8},
            ),
            (
                [
                    Product("P1", "brand1", 100, 3.0),
                    Product("P2", "brand1", 200, 5.0),
                ],
                1,
                {"brand1": 4.0},
            ),
        ],
    )
    def test_calculate_various_scenarios(
        self, calculator, products, expected_count, expected_ratings
    ):
        result = calculator.calculate(products)

        assert len(result) == expected_count
        for stats in result:
            assert stats.average_rating == expected_ratings[stats.brand]

    def test_calculate_empty_list(self, calculator):
        result = calculator.calculate([])
        assert result == []

    @pytest.mark.parametrize(
        "products,expected_order",
        [
            (
                [
                    Product("Low", "low", 100, 3.0),
                    Product("High", "high", 200, 5.0),
                    Product("Mid", "mid", 150, 4.0),
                ],
                ["high", "mid", "low"],
            ),
        ],
    )
    def test_sorting_order(self, calculator, products, expected_order):
        result = calculator.calculate(products)
        actual_order = [stats.brand for stats in result]
        assert actual_order == expected_order
