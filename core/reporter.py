"""
Модуль для генерации различных типов отчетов.
"""

from typing import List, Dict, Any
from tabulate import tabulate


def generate_report(report_type: str, brand_data: List[Dict[str, Any]]) -> str:
    """
    Генерирует отчет в виде таблицы на основе переданных данных.

    :param report_type:  Тип отчета
    :param brand_data: Данные о брендах и статистиках

    :return: Строка с отформатированной таблицей отчета

    :raise ValueError: Если передан неизвестный тип отчета
    """
    if report_type == "average-rating":
        return _generate_average_rating_report(brand_data)
    else:
        raise ValueError('Неизвестный тип отчета: %s' % report_type)


def _generate_average_rating_report(brand_data: List[Dict[str, Any]]) -> str:
    """
    Генерирует отчет со средним рейтингами брендов.

    :param brand_data: Данные о брендах и их средних рейтингах

    :return: Строка с отформатированной таблицей
    """
    # Подготавливаем данные для таблицы
    table_data = []
    for index, brand_info in enumerate(brand_data, start=1):
        table_data.append([
            index,
            brand_info['brand'],
            brand_info['average_rating'],
        ])

    # Создаем таблицу
    table = tabulate(
        table_data,
        headers=['', 'brand', 'rating'],
        tablefmt='grid',
        stralign='center',
        numalign='center',
    )

    return table
