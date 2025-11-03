"""
Тесты для модуля чтения CSV файлов.
"""

import os
import tempfile

import pytest

from core.reader import read_product_files


class TestReadProductFiles:
    """Тесты для функции read_product_files."""

    def test_read_single_valid_file(self, temp_csv_file):
        """Тест чтения одного корректного CSV файла."""
        csv_content = (
            "name,brand,price,rating\n"
            "iPhone 15 Pro,apple,999,4.9\n"
            "Galaxy S23 Ultra,samsung,1199,4.8\n"
            "Redmi Note 12,xiaomi,199,4.6"
        )

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])

        assert len(products) == 3
        assert products[0]['name'] == "iPhone 15 Pro"
        assert products[0]['brand'] == "apple"  # Проверяем lower()
        assert products[0]['price'] == 999.0
        assert products[0]['rating'] == 4.9

        assert products[1]['brand'] == "samsung"
        assert products[2]['brand'] == "xiaomi"

    def test_read_multiple_files(self):
        """Тест чтения нескольких CSV файлов."""
        csv_content1 = (
            "name,brand,price,rating\n"
            "Product1,brand1,100,4.5"
        )

        csv_content2 = (
            "name,brand,price,rating\n"
            "Product2,brand2,200,4.0"
        )

        temp_files = []
        try:
            for i, content in enumerate([csv_content1, csv_content2]):
                with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{i}.csv', delete=False) as f:
                    f.write(content)
                    temp_files.append(f.name)

            products = read_product_files(temp_files)

            assert len(products) == 2
            brands = [product['brand'] for product in products]
            assert "brand1" in brands
            assert "brand2" in brands

        finally:
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

    def test_file_not_found(self):
        """Тест обработки отсутствующего файла."""
        file_name = "nonexistent.csv"
        with pytest.raises(FileNotFoundError, match=f'Файл {file_name} не найден'):
            read_product_files([file_name])

    def test_missing_required_columns(self, temp_csv_file):
        """Тест отсутствия обязательных колонок."""
        csv_content = (
            "name,price,rating\n"
            "Product1,100,4.5"
        )

        temp_file = temp_csv_file(csv_content)

        with pytest.raises(ValueError, match=f'не содержит все необходимые колонки'):
            read_product_files([temp_file])

    def test_empty_file(self, temp_csv_file):
        """Тест пустого файла."""
        temp_file = temp_csv_file("")

        with pytest.raises(ValueError, match='не содержит заголовков'):
            read_product_files([temp_file])

    def test_file_with_only_header(self, temp_csv_file):
        """Тест файла только с заголовками."""
        csv_content = "name,brand,price,rating"

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])
        assert products == []

    def test_whitespace(self, temp_csv_file):
        """Тест обработки пробелов в данных."""
        csv_content = (
            "name,brand,price,rating\n"
            "  iPhone 15 Pro  ,  apple  ,  999  ,  4.9  \n"
            "Galaxy S23 Ultra , samsung,1199,4.8"
        )

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])

        assert len(products) == 2
        assert products[0]['name'] == "iPhone 15 Pro"
        assert products[0]['brand'] == "apple"  # Без пробелов и lower()
        assert products[0]['price'] == 999.0
        assert products[0]['rating'] == 4.9

    def test_empty_rows_skipping(self, temp_csv_file):
        """Тест пропуска пустых строк."""
        csv_content = (
            "name,brand,price,rating\n"
            "iPhone,apple,999,4.9\n"
            ",,,\n"
            "Galaxy,samsung,1199,4.8\n"
            "   ,   ,   ,\n"
            "Redmi,xiaomi,199,4.6"
        )

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])

        # Должны быть прочитаны только 3 корректные строки
        assert len(products) == 3
        assert products[0]['brand'] == "apple"
        assert products[1]['brand'] == "samsung"
        assert products[2]['brand'] == "xiaomi"

    def test_invalid_rating_range(self, temp_csv_file):
        """Тест некорректного диапазона рейтинга."""
        csv_content = (
            "name,brand,price,rating\n"
            "Product1,Brand1,100,5.1"
        )  # Рейтинг > 5

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])

        # Строка с некорректным рейтингом должна быть пропущена
        assert len(products) == 0

    def test_invalid_numeric_values(self, temp_csv_file):
        """Тест некорректных числовых значений."""
        csv_content = (
            "name,brand,price,rating\n"
            "Product1,brand1,invalid_price,4.5\n"
            "Product2,brand2,200,invalid_rating"
        )

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])

        # Обе строки должны быть пропущены из-за некорректных чисел
        assert len(products) == 0

    def test_mixed_valid_invalid_rows(self, temp_csv_file):
        """Тест смеси корректных и некорректных строк."""
        csv_content = (
            "name,brand,price,rating\n"
            "Valid1,brand1,100,4.5\n"
            ",,,\n"
            "Invalid2,,200,4.0\n"
            "Valid3,brand3,300,4.8\n"
            "Invalid4,brand4,invalid,4.2"
        )

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])

        # Должны быть прочитаны только 2 корректные строки
        assert len(products) == 2
        assert products[0]['brand'] == "brand1"
        assert products[1]['brand'] == "brand3"

    def test_whitespace_validation_in_reader(self, temp_csv_file):
        """Тест валидации пробелов при чтении файла."""
        csv_content = (
            "name,brand,price,rating\n"
            " ,Apple,999,4.9"  # Пробелы в названии
        )

        temp_file = temp_csv_file(csv_content)
        products = read_product_files([temp_file])
        # Строка должна быть пропущена из-за failed валидации
        assert len(products) == 0
