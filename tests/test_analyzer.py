import pytest

from core.analyzer import BrandRatingAnalyzer


@pytest.fixture
def analyzer() -> BrandRatingAnalyzer:
    return BrandRatingAnalyzer()


class TestBrandRatingAnalyzer:
    """Тесты фасада анализатора."""

    @pytest.mark.parametrize(
        "file_paths,report_type,expected_contains",
        [
            (["tests/fixtures/sample.csv"], "average-rating", ["brand", "rating"]),
        ],
    )
    def test_analyze_valid_data(
        self, analyzer, file_paths, report_type, expected_contains
    ):
        result = analyzer.analyze(file_paths, report_type)

        for expected in expected_contains:
            assert expected in result

    def test_get_available_reports(self, analyzer):
        reports = analyzer.get_available_reports()
        assert "average-rating" in reports
        assert isinstance(reports, list)
