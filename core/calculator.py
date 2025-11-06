"""
Модуль для вычисления статистик по брендам.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from collections import defaultdict

from core.models import Product, BrandStatistics


class StatisticsCalculator(ABC):
    """Абстрактный базовый класс для расчета статистик."""

    @abstractmethod
    def calculate(self, products: List[Product]) -> List[BrandStatistics]:
        pass


class BrandRatingCalculator(StatisticsCalculator):
    """Калькулятор средних рейтингов по брендам."""

    def calculate(self, products: List[Product]) -> List[BrandStatistics]:
        if not products:
            return []

        brand_stats = self._aggregate_brand_data(products)
        return self._create_brand_statistics(brand_stats)

    @staticmethod
    def _aggregate_brand_data(products: List[Product]) -> Dict[str, dict]:
        brand_stats = defaultdict(lambda: {"total_rating": 0, "count": 0})

        for product in products:
            brand_stats[product.brand]['total_rating'] += product.rating
            brand_stats[product.brand]['count'] += 1

        return brand_stats

    @staticmethod
    def _create_brand_statistics(brand_stats: dict) -> List[BrandStatistics]:
        statistics = []

        for brand, stats in brand_stats.items():
            avg_rating = stats['total_rating'] / stats['count']
            statistics.append(BrandStatistics(
                brand=brand,
                average_rating=avg_rating,
                product_count=stats['count'],
            ))

        return sorted(statistics, key=lambda x: x.average_rating, reverse=True)
