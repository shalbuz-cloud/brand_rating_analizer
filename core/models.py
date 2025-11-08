"""
Data Transfer Objects (DTO) для проекта.
"""

from dataclasses import dataclass


@dataclass
class Product:
    """DTO для продукта."""

    name: str
    brand: str
    price: float
    rating: float

    def __post_init__(self) -> None:
        """Валидация после инициализации."""
        if not 0 <= self.rating <= 5:
            raise ValueError(
                "Рейтинг должен быть от 0 до 5, получено: %.2f" % self.rating
            )


@dataclass
class BrandStatistics:
    """DTO для статистики бренда."""

    brand: str
    average_rating: float
    product_count: int

    def __post_init__(self) -> None:
        """Округление рейтинга после инициализации."""
        self.average_rating = round(self.average_rating, 2)
