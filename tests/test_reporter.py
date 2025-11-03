"""
Тесты для модуля генерации отчетов.
"""

import pytest

from core.reporter import generate_report, _generate_average_rating_report


class TestGenerateReport:
    """Тесты для функции generate_report."""

    def test_average_rating_report_valid(self):
        """Тест генерации отчета по средним рейтингам."""
        brand_data = [
            {"brand": "apple", "average_rating": 4.55, "product_count": 10},
            {"brand": "samsung", "average_rating": 4.53, "product_count": 8},
            {"brand": "xiaomi", "average_rating": 4.37, "product_count": 15},
        ]

        report = generate_report('average-rating', brand_data)

        # Проверяем, что отчет содержит ожидаемые данные
        assert "apple" in report
        assert "4.55" in report
        assert "samsung" in report
        assert "4.53" in report
        assert "xiaomi" in report
        assert "4.37" in report
        assert "brand" in report
        assert "rating" in report

    def test_unknown_report_type(self):
        """Тест неизвестного типа отчета."""
        brand_data = []

        with pytest.raises(ValueError, match='Неизвестный тип отчета: unknown-report'):
            generate_report('unknown-report', brand_data)

    def test_empty_brand_data(self):
        """Тест с пустыми данными о брендах."""
        brand_data = []

        report = generate_report('average-rating', brand_data)

        # Отчет должен создаться даже для пустых данных
        assert report is not None
        assert "brand" in report  # Заголовки должны присутствовать

    def test_report_structure(self):
        """Тест структуры отчета."""
        brand_data = [
            {"brand": "apple", "average_rating": 4.8, "product_count": 2},
            {"brand": "samsung", "average_rating": 4.6, "product_count": 3},
        ]

        report = generate_report('average-rating', brand_data)

        # Проверяем базовую структуру таблицы
        lines = report.split('\n')
        assert len(lines) > 5  # Должно быть несколько строк в таблице

        # Проверяем наличие заголовков
        header_line = lines[1]
        assert "brand" in header_line.lower()
        assert "rating" in header_line.lower()

    def test_special_characters_in_brand_names(self):
        """Тест специальных символов в названиях брендов."""
        brand_data = [
            {'brand': 'apple-inc', 'average_rating': 4.8, 'product_count': 2},
            {'brand': 'samsung&co', 'average_rating': 4.6, 'product_count': 3},
            {'brand': 'huawei (china)', 'average_rating': 4.4, 'product_count': 1},
        ]

        report = generate_report('average-rating', brand_data)

        # Проверяем, что все специальные символы корректно отображаются
        assert "apple-inc" in report
        assert "samsung&co" in report
        assert "huawei (china)" in report


class TestGenerateAverageRatingReport:
    """Тесты для внутренней функции _generate_average_rating_report."""

    def test_basic_functionality(self):
        """Тест базовой функциональности."""
        brand_data = [
            {'brand': 'apple', 'average_rating': 4.8, 'product_count': 2},
            {'brand': 'samsung', 'average_rating': 4.6, 'product_count': 3},
        ]

        report = _generate_average_rating_report(brand_data)

        # Проверяем порядковые номера
        assert "1" in report
        assert "2" in report
        assert "apple" in report
        assert "samsung" in report
        assert "4.8" in report
        assert "4.6" in report

    def test_sorting_preserved(self):
        """Тест, что сортировка данных сохраняется в отчете."""
        brand_data = [
            {'brand': 'high', 'average_rating': 5.0, 'product_count': 1},
            {'brand': 'medium', 'average_rating': 4.0, 'product_count': 1},
            {'brand': 'low', 'average_rating': 3.0, 'product_count': 1},
        ]

        report = _generate_average_rating_report(brand_data)

        # Находим позиции брендов в отчете
        report_lines = report.split('\n')
        high_index = None
        medium_index = None
        low_index = None

        for i, line in enumerate(report_lines):
            if "high" in line:
                high_index = i
            elif "medium" in line:
                medium_index = i
            elif "low" in line:
                low_index = i

        # high должен быть выше medium, medium выше low
        assert all(value is not None for value in [high_index, medium_index, low_index])
        assert high_index < medium_index < low_index

    def test_table_format(self):
        """Тест формата таблицы."""
        brand_data = [
            {"brand": "test", "average_rating": 4.5, "product_count": 1},
        ]

        report = _generate_average_rating_report(brand_data)

        # Проверяем что это действительно таблица в grid формате
        assert "+" in report  # Границы ячеек
        assert "|" in report  # Разделители колонок
