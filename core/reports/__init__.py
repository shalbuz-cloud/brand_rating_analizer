"""
Модуль системы отчетов с использованием абстрактных классов.
"""

from .average_rating import AverageRatingReport
from .base import Report, ReportFactory

# Регистрируем отчеты
ReportFactory.register("average-rating", AverageRatingReport)

# Для обратной совместимости
__all__ = ["Report", "ReportFactory", "AverageRatingReport"]
