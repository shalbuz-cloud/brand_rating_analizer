"""
Модуль для вычисления статистик по брендам.
"""
from typing import List, Dict, Any
from collections import defaultdict


def calculate_brand_ratings(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Вычисляет средний рейтинг для каждого бренда.

    :param products: Список продуктов с информацией о брендах и рейтингах
    :return: Отсортированный список словарей с брендами и их средним рейтингом
    """
    brand_stats = defaultdict(lambda: {"total_rating": 0, "count": 0})

    # Суммируем рейтинги и подсчитываем количество товаров для каждого бренда
    for product in products:
        brand = product['brand']
        rating = product['rating']

        brand_stats[brand]['total_rating'] += rating
        brand_stats[brand]['count'] += 1

    # Вычисляем средние рейтинги и формируем результат
    result = []
    for brand, stats in brand_stats.items():
        average_rating = stats['total_rating'] / stats['count']
        result.append({
            "brand": brand,
            "average_rating": round(average_rating, 2),
            "product_count": stats['count']  # Может пригодиться для расширения функционала,
        })

    # Сортируем по убыванию рейтинга (от высшего к низшему)
    result.sort(key=lambda x: x['average_rating'], reverse=True)

    return result
