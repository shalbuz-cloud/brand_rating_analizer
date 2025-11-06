"""
Модуль системы отчетов с использованием абстрактных классов.
"""

from abc import ABC, abstractmethod
from typing import List

from core.models import BrandStatistics


class Report(ABC):
    """Абстрактный базовый класс для всех отчетов."""

    @abstractmethod
    def generate(self, data: List[BrandStatistics]) -> str:
        """Генерирует отчет на основе данных."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает название отчета."""
        pass


class AverageRatingReport(Report):
    """Отчет по средним рейтингам брендов."""

    @property
    def name(self) -> str:
        return "average-rating"

    def generate(self, data: List[BrandStatistics]) -> str:
        from tabulate import tabulate

        table_data = []
        for index, stats in enumerate(data, start=1):
            table_data.append([index, stats.brand, stats.average_rating])

        return tabulate(
            table_data,
            headers=["", "brand", "rating"],
            tablefmt='grid',
            stralign='center',
            numalign='center',
        )


class ReportFactory:
    """Фабрика для создания отчетов."""

    _reports = {
        "average-rating": AverageRatingReport,
    }

    @classmethod
    def create(cls, report_type: str) -> Report:
        """Создает отчет по типу."""
        if report_type not in cls._reports:
            raise ValueError('Unknown report type: %s' % report_type)
        return cls._reports[report_type]()

    @classmethod
    def register(cls, report_type: str, report_class: type[Report]) -> None:
        """Регистрирует новый тип отчета."""
        cls._reports[report_type] = report_class

    @classmethod
    def get_available_reports(cls) -> List[str]:
        """Возвращает список доступных отчетов."""
        return list(cls._reports.keys())
