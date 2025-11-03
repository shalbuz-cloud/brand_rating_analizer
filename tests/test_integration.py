"""
Интеграционные тесты для проверки взаимодействия модулей.
"""

from core.reader import read_product_files
from core.calculator import calculate_brand_ratings
from core.reporter import generate_report


class TestIntegration:
    """Интеграционные тесты полного workflow."""

    def test_full_workflow(self, temp_csv_file):
        """Тест полного workflow от чтения файлов до генерации отчета."""
        csv_content = (
            "name,brand,price,rating\n"
            "iPhone 15 Pro,Apple,999,4.9\n"
            "Galaxy S23 Ultra,Samsung,1199,4.8\n"
            "Redmi Note 12,Xiaomi,199,4.6\n"
            "iPhone 14,Apple,799,4.7"
        )

        temp_file = temp_csv_file(csv_content)

        # Шаг 1: Чтение файлов
        products = read_product_files([temp_file])
        assert len(products) == 4

        # Шаг 2: Расчет статистик
        brand_ratings = calculate_brand_ratings(products)
        assert len(brand_ratings) == 3

        # Проверяем расчеты
        apple_data = next(item for item in brand_ratings if item['brand'] == 'apple')
        assert apple_data['average_rating'] == 4.8  # (4.9 + 4.7) / 2
        assert apple_data['product_count'] == 2

        # Шаг 3: Генерация отчета "average_rating"
        report = generate_report('average-rating', brand_ratings)
        assert "apple" in report
        assert "4.8" in report
        assert "samsung" in report
        assert "xiaomi" in report

    def test_workflow_with_empty_data(self, temp_csv_file):
        """Тест workflow c пустыми данными."""
        csv_content = "name,brand,price,rating"
        temp_file = temp_csv_file(csv_content)

        products = read_product_files([temp_file])
        assert products == []

        brand_ratings = calculate_brand_ratings(products)
        assert brand_ratings == []

        report = generate_report('average-rating', brand_ratings)
        assert report is not None
