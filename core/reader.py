"""
Модуль для чтения и обработки CSV файлов с данными о продуктах.
"""

import csv
from typing import List, Dict, Any

from core.debug import debug_print
from core.utils.validators import is_empty_row, validate_required_fields, validate_rating
from core.utils.converters import safe_strip, safe_float


def read_product_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Читает данные о продуктах из одного или нескольких CSV файлов.
    :param file_paths: Список путей к CSV файлам
    :return: Список словарей с данными о продуктах

    :raises
        FileNotFoundError: Если какой-либо файл не найден
        ValueError: Если данные в файле некорректны
    """
    all_products = []

    for file_path in file_paths:
        try:
            debug_print('Обработка файла: %s' % file_path)

            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    raise ValueError(
                        'Файл %s не содержит заголовков или имеет неверный формат'
                        % file_path
                    )

                # Проверяем, что все необходимые колонки присутствуют
                required_columns = ["name", "brand", "price", "rating"]
                missing_columns = [col for col in required_columns if col not in reader.fieldnames]
                if missing_columns:
                    raise ValueError(
                        'Файл %s не содержит все необходимые колонки. '
                        'Отсутствуют: %s. '
                        'Найдены: %s'
                        % (file_path, missing_columns, list(reader.fieldnames))
                    )

                processed_rows = 0
                skipped_rows = 0

                # Читаем и обрабатываем каждую строку
                for row_num, row in enumerate(reader, start=2):  # 1я строка - заголовок

                    try:
                        # Пропускаем пустые строки
                        if is_empty_row(row):
                            debug_print(
                                'Предупреждение: Пропуск пустой строки %d в файле %s'
                                % (row_num, file_path)
                            )
                            skipped_rows += 1
                            continue

                        # Валидируем сырые данные
                        raw_product = {
                            "name": row.get('name'),
                            "brand": row.get('brand'),
                            "price": row.get('price'),
                            "rating": row.get('rating'),
                        }
                        validate_required_fields(raw_product)

                        # Очистка и преобразование
                        product = {
                            "name": safe_strip(raw_product['name']),
                            "brand": safe_strip(raw_product['brand']),
                            "price": safe_float(raw_product['price']),
                            "rating": safe_float(raw_product['rating']),
                        }

                        # Дополнительная валидация на очищенных числовых данных
                        validate_rating(product['rating'])

                        all_products.append(product)
                        processed_rows += 1

                    except (ValueError, KeyError) as e:
                        debug_print(
                            'Предупреждение: Пропуск строки %d в файле %s: %s'
                            % (row_num, file_path, e)
                        )
                        skipped_rows += 1
                        continue

                debug_print(
                    'Файл %s: обработано %d строк, пропущено %d строк'
                    % (file_path, processed_rows, skipped_rows)
                )

        except FileNotFoundError:
            raise FileNotFoundError('Файл %s не найден' % file_path)

        except Exception as e:
            raise ValueError('Ошибка при чтении файла %s: %s' % (file_path, e))

    return all_products
