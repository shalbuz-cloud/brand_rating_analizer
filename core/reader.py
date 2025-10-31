"""
Модуль для чтения и обработки CSV файлов с данными о продуктах.
"""

import csv
from typing import List, Dict, Any


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
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)  # TODO: Вспомнить библиотеку CSV

                # Проверяем, что все необходимые колонки присутствуют
                required_columns = ["name", "brand", "price", "rating"]
                if not all(column in reader.fieldnames for column in required_columns):
                    raise ValueError(
                        'Файл %s не содержит все необходимые колонки: %s'
                        % (file_path, required_columns)
                    )

                # Чтение и обработка файла
                for row_num, row in enumerate(reader, start=2):  # 1я строка - заголовок

                    try:
                        # Валидируем и преобразуем данные
                        product = {
                            "name": row['name'].strip(),
                            "brand": row['brand'].strip().lower(),
                            "price": float(row['price']),
                            "rating": float(row['rating']),
                        }

                        # Проверяем корректность рейтинга (должен быть от 0 до 5)
                        if not 0 <= product['rating'] <= 5:
                            raise ValueError(
                                'Рейтинг должен быть отт 0 до 5, получено: %d'
                                % product['rating']
                            )
                        all_products.append(product)

                    except (ValueError, KeyError) as e:
                        print(
                            'Предупреждение: Пропуск строки %d в файле %s: %s'
                            % (row_num, file_path, e)
                        )
                        continue

        except FileNotFoundError:
            raise FileNotFoundError('Файл %s не найден' % file_path)

        except Exception as e:
            raise ValueError('Ошибка при чтении файла %s: %s' % (file_path, e))

    return all_products
