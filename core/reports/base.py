"""
Базовые классы для системы отчетов.
"""

from abc import ABC, abstractmethod

from core.models import BrandStatistics


class Report(ABC):
    """Абстрактный базовый класс для всех отчетов."""

    @abstractmethod
    def generate(self, data: list[BrandStatistics]) -> str:
        """Генерирует отчет на основе данных."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает название отчета."""
        pass


class ReportFactory:
    """Фабрика для создания отчетов."""

    _reports: dict[str, type[Report]] = {}

    @classmethod
    def create(cls, report_type: str) -> Report:
        """Создает отчет по типу."""
        if report_type not in cls._reports:
            raise ValueError("Unknown report type: %s" % report_type)
        return cls._reports[report_type]()

    @classmethod
    def register(cls, report_type: str, report_class: type[Report]) -> None:
        """Регистрирует новый тип отчета."""
        cls._reports[report_type] = report_class

    @classmethod
    def get_available_reports(cls) -> list[str]:
        """Возвращает список доступных отчетов."""
        return list(cls._reports.keys())
