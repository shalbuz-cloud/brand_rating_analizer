"""
Модуль для вычисления статистик по брендам.
"""

from abc import ABC, abstractmethod
from collections import defaultdict

from core.models import BrandStatistics, Product


class StatisticsCalculator(ABC):
    """Абстрактный базовый класс для расчета статистик."""

    @abstractmethod
    def calculate(self, products: list[Product]) -> list[BrandStatistics]:
        pass


class CalculatorFactory:
    """Фабрика для создания калькулятора статистик."""

    _calculators: dict[str, type[StatisticsCalculator]] = {}

    @classmethod
    def create(cls, calculator_type: str) -> StatisticsCalculator:
        """
        Создает калькулятор указанного типа.

        :param calculator_type: Тип калькулятора

        :return: Объект калькулятора

        :raise ValueError: Если тип калькулятора неизвестен
        """
        if calculator_type not in cls._calculators:
            raise ValueError("Unknown calculator type: %s" % calculator_type)
        return cls._calculators[calculator_type]()

    @classmethod
    def register(
        cls, calculator_type: str, calculator_class: type[StatisticsCalculator]
    ) -> None:
        """
        Регистрирует новый тип калькулятора.

        :param calculator_type: Идентификатор калькулятора
        :param calculator_class: Класс калькулятора
        """
        cls._calculators[calculator_type] = calculator_class

    @classmethod
    def get_available_calculators(cls) -> list[str]:
        """Возвращает список доступных калькуляторов."""
        return list(cls._calculators.keys())


def register_calculator(calculator_type: str):  # type: ignore
    """
    Декоратор для автоматической регистрации калькуляторов в фабрике.

    :param calculator_type: Тип калькулятора для регистрации
    """

    def decorator(cls: type[StatisticsCalculator]):  # type: ignore
        CalculatorFactory.register(calculator_type, cls)
        return cls

    return decorator


@register_calculator("average-rating")
class BrandRatingCalculator(StatisticsCalculator):
    """Калькулятор средних рейтингов по брендам."""

    def calculate(self, products: list[Product]) -> list[BrandStatistics]:
        if not products:
            return []

        brand_stats = self._aggregate_brand_data(products)
        return self._create_brand_statistics(brand_stats)

    @staticmethod
    def _aggregate_brand_data(products: list[Product]) -> dict[str, dict]:
        brand_stats: dict[str, dict] = defaultdict(
            lambda: {"total_rating": 0, "count": 0}
        )

        for product in products:
            brand_stats[product.brand]["total_rating"] += product.rating
            brand_stats[product.brand]["count"] += 1

        return brand_stats

    @staticmethod
    def _create_brand_statistics(brand_stats: dict) -> list[BrandStatistics]:
        statistics = []

        for brand, stats in brand_stats.items():
            avg_rating = stats["total_rating"] / stats["count"]
            statistics.append(
                BrandStatistics(
                    brand=brand,
                    average_rating=avg_rating,
                    product_count=stats["count"],
                )
            )

        return sorted(statistics, key=lambda x: x.average_rating, reverse=True)
