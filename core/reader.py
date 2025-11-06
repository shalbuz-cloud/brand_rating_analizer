"""
Модуль для чтения и обработки CSV файлов с данными о продуктах.
"""

from abc import ABC, abstractmethod
import csv
from typing import List

from core.debug import debug_print
from core.models import Product
from core.utils.validators import DataValidator
from core.utils.converters import DataConverter


class FileReader(ABC):
    """Абстрактный базовый класс для чтения файлов."""

    @abstractmethod
    def read(self, file_paths: List[str]) -> List[Product]:
        pass


class CSVProductReader(FileReader):
    """Реализация чтения CSV файлов с продуктами."""

    def __init__(self, validator: DataValidator, converter: DataConverter):
        self.validator = validator
        self.converter = converter

    def read(self, file_paths: List[str]) -> List[Product]:
        """
        Читает данные о продуктах из одного или нескольких CSV файлов.

        :param file_paths: Список путей к CSV файлам

        :return: Список объектов Product

        :raises
            FileNotFoundError: Если файл не найден
            ValueError: Если данные некорректны
        """
        products: List[Product] = []

        for file_path in file_paths:
            debug_print('Обработка файла: %s' % file_path)
            products.extend(self._read_single_file(file_path))

        debug_print('Всего прочитано %d записей о продуктах' % len(products))
        return products

    def _read_single_file(self, file_path: str) -> List[Product]:
        """
        Читает данные из одного CSV файла.

        :param file_path: Путь к CSV файлу

        :return: Список объектов Product из файла
        """

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                if not reader.fieldnames:
                    raise ValueError('File %s has no headers' % file_path)

                self._validate_headers(reader.fieldnames, file_path)
                return self._process_rows(reader, file_path)

        except FileNotFoundError:
            raise FileNotFoundError('File %s not found' % file_path)
        except Exception as e:
            raise ValueError('Error reading file %s: %s' % (file_path, e))

    @staticmethod
    def _validate_headers(headers: List[str], file_path: str) -> None:
        required_columns = ["name", "brand", "price", "rating"]
        missing = [col for col in required_columns if col not in headers]

        if missing:
            raise ValueError(
                'File %s missing required columns: %s'
                'Found: %s'
                % (file_path, missing, headers)
            )

    def _process_rows(self, reader: csv.DictReader, file_path: str) -> List[Product]:
        products = []
        processed_rows = 0
        skipped_rows = 0

        for row_num, row in enumerate(reader, start=2):  # 1st line - headers
            try:
                if self.validator.is_empty_row(row):
                    debug_print(
                        'Предупреждение: Пропуск пустой строки %d в файле %s'
                        % (row_num, file_path)
                    )
                    skipped_rows += 1
                    continue

                product = self._create_product_from_row(row)
                products.append(product)
                processed_rows += 1

            except (ValueError, KeyError) as e:
                debug_print(
                    'Предупреждение: Пропуск пустой строки %d в файле %s'
                    % (row_num, file_path)
                )
                skipped_rows += 1
                continue

        debug_print(
            'Файл %s: обработано %d строк, пропущено %d строк'
            % (file_path, processed_rows, skipped_rows)
        )
        return products

    def _create_product_from_row(self, row: dict) -> Product:
        raw_data = {
            "name": row.get('name'),
            "brand": row.get('brand'),
            "price": row.get('price'),
            "rating": row.get('rating'),
        }

        self.validator.validate_required_fields(raw_data)

        processed_data = {
            "name": self.converter.safe_strip(raw_data['name']),
            "brand": self.converter.safe_strip(raw_data['brand']).lower(),
            "price": self.converter.safe_float(raw_data['price']),
            "rating": self.converter.safe_float(raw_data['rating']),
        }

        self.validator.validate_rating(processed_data['rating'])

        return Product(**processed_data)
