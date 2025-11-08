import pytest

from core.models import BrandStatistics
from core.reports import AverageRatingReport, ReportFactory


class TestReportFactory:
    """Тесты фабрики отчетов."""

    def test_create_existing_report(self):
        """Тест создания существующего отчета."""
        report = ReportFactory.create("average-rating")
        assert isinstance(report, AverageRatingReport)
        assert report.name == "average-rating"

    def test_create_nonexistent_report(self):
        """Тест создания несуществующего отчета."""
        with pytest.raises(ValueError, match="Unknown report type: nonexistent-report"):
            ReportFactory.create("nonexistent-report")

    def test_get_available_reports(self):
        """Тест получения доступных отчетов."""
        reports = ReportFactory.get_available_reports()
        assert "average-rating" in reports
        assert isinstance(reports, list)

    def test_register_new_report(self):
        """Тест регистрации нового отчета."""

        class TestReport(AverageRatingReport):
            @property
            def name(self):
                return "test-report"

        ReportFactory.register("test-report", TestReport)
        assert "test-report" in ReportFactory.get_available_reports()

        report = ReportFactory.create("test-report")
        assert report.name == "test-report"


class TestAverageRatingReport:
    """Тесты отчета по средним рейтингам."""

    @pytest.fixture
    def report(self):
        return AverageRatingReport()

    @pytest.mark.parametrize(
        "statistics,expected_brands,expected_ratings",
        [
            (
                [
                    BrandStatistics("apple", 4.8, 2),
                    BrandStatistics("samsung", 4.6, 3),
                ],
                ["apple", "samsung"],
                {"apple": "4.8", "samsung": "4.6"},
            ),
            (
                [
                    BrandStatistics("brand1", 5.0, 1),
                    BrandStatistics("brand2", 3.5, 1),
                ],
                ["brand1", "brand2"],
                {
                    "brand1": ["5", "5.0"],
                    "brand2": "3.5",
                },  # Разные варианты форматирования
            ),
        ],
    )
    def test_generate_report(
        self, report, statistics, expected_brands, expected_ratings
    ):
        """Гибкий тест генерации отчета с учетом форматирования чисел."""
        result = report.generate(statistics)

        for brand in expected_brands:
            assert brand in result

        # Проверяем рейтинги с учетом возможного форматирования
        for brand, expected_rating in expected_ratings.items():
            if isinstance(expected_rating, list):
                # Если несколько форматов форматирования
                found = any(rating in result for rating in expected_rating)
                assert found, "None of %s found for %s in: %s" % (
                    expected_rating,
                    brand,
                    result,
                )
            else:
                assert expected_rating in result

    def test_generate_empty_report(self, report):
        """Тест генерации отчета с пустыми данными."""
        result = report.generate([])
        assert "brand" in result
        assert "rating" in result
