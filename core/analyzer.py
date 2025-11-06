from typing import List

from core.reader import CSVProductReader
from core.calculator import BrandRatingCalculator
from core.reports import ReportFactory
from core.utils.validators import DataValidator
from core.utils.converters import DataConverter


class BrandRatingAnalyzer:
    """Фасад для анализа рейтингов брендов."""

    def __init__(self):
        self.reader = CSVProductReader(DataValidator(), DataConverter())
        self.calculator = BrandRatingCalculator()

    def analyze(self, file_paths: List[str], report_type: str) -> str:
        products = self.reader.read(file_paths)
        statistics = self.calculator.calculate(products)
        report = ReportFactory.create(report_type)
        return report.generate(statistics)

    @staticmethod
    def get_available_reports() -> List[str]:
        return ReportFactory.get_available_reports()
