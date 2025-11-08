from core.models import BrandStatistics

from .base import Report


class AverageRatingReport(Report):
    """Отчет по средним рейтингам брендов."""

    @property
    def name(self) -> str:
        return "average-rating"

    def generate(self, data: list[BrandStatistics]) -> str:
        from tabulate import tabulate

        table_data = []
        for index, stats in enumerate(data, start=1):
            table_data.append([index, stats.brand, stats.average_rating])

        return tabulate(
            table_data,
            headers=["", "brand", "rating"],
            tablefmt="grid",
            stralign="center",
            numalign="center",
        )
