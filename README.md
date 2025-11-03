# Brand Rating Analyzer

Скрипт для анализа рейтингов брендов из CSV файлов.

## Установка

1. Клонируйте репозиторий

```bash
git clone git@github.com:shalbuz-cloud/brand_rating_analizer.git

# Перейдите в каталог проекта
cd brand_rating_analizer
```

2. Установите зависимости с помощью Poetry:

```bash
poetry install
```

3. Активируйте виртуальное окружение:

```bash
poetry shell
```

## Использование

```bash
# Активируйте виртуальное окружение если еще не активировано
poetry shell

# Запуск скрипта (только финальный отчет)
python main.py --files products1.csv products2.csv --report average-rating

# Запуск скрипта - Debug режим (все принты + отчет)
python main.py --fils products1.csv --report average-rating --debug
```

## Запуск тестов

```bash
# Все тесты
poetry run pytest tests/

# Тесты с покрытием
poetry run pytest --cov=core tests/

# Конкретный тестовый файл
poetry run pytest tests/test_reader.py -v
```

## Формат CSV файлов

CSV файлы должны содержать следующие колонки:

- `name` - название продукта
- `brand` - бренд продукта
- `price` - цена продукта
- `rating` - рейтинг продукта (от 0 до 5)

Пример:

```csv
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
```

## Структура проекта

```text
brand_rating_analyzer/
├── main.py                 # Основной скрипт
├── pyproject.toml          # Конфигурация Poetry
├── core/                   # Основные модули
│   ├── __init__.py
│   ├── reader.py           # Чтение CSV файлов
│   ├── calculator.py       # Расчет статистик
│   ├── reporter.py         # Генерация отчетов
│   └── utils/              # Вспомогательные утилиты
├── tests/                  # Тесты
└── README.md
```

## Пример вывода

```text
+----+----------+---------+
|    |  brand   | rating  |
+====+==========+=========+
| 1  |  apple   |  4.8    |
+----+----------+---------+
| 2  | samsung  |  4.65   |
+----+----------+---------+
| 3  | xiaomi   |  4.5    |
+----+----------+---------+
```

## Добавление новых отчетов

Архитектура проекта позволяет легко добавлять новые типы отчетов.

1. Добавьте новую функцию отчета в `core/reporter.py`

```python
def _generate_average_price_report(brand_data: List[Dict[str, Any]]) -> str:
    """
    Генерирует отчет со средними ценами по брендам.
    """
    table_data = []
    for index, brand_info in enumerate(brand_data, start=1):
        table_data.append([
            index,
            brand_info['brand'],
            brand_info['average_price'],
        ])

    table = tabulate(
        table_data,
        headers=['', 'brand', 'average_price'],
        tablefmt='grid',
        stralign='center',
        numalign='center',
    )
    return table
```

2. Обновите функцию `generate_report`

```python
def generate_report(report_type: str, brand_data: List[Dict[str, Any]]) -> str:
    if report_type == "average-rating":
        return _generate_average_rating_report(brand_data)
    elif report_type == "average-price":  # Новый тип отчета
        return _generate_average_price_report(brand_data)
    else:
        raise ValueError('Неизвестный тип отчета: %s' % report_type)
```

3. Обновите калькулятор для расчета новых метрик

```python
def calculate_brand_prices(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Вычисляет среднюю цену для каждого бренда.
    """
    brand_stats = defaultdict(lambda: {"total_price": 0, "count": 0})
    
    for product in products:
        brand = product['brand'].strip().lower()
        price = product['price']
        
        brand_stats[brand]['total_price'] += price
        brand_stats[brand]['count'] += 1
    
    result = []
    for brand, stats in brand_stats.items():
        average_price = stats['total_price'] / stats['count']
        result.append({
            "brand": brand,
            "average_price": round(average_price, 2),
            "product_count": stats['count']
        })
    
    result.sort(key=lambda x: x['average_price'], reverse=True)
    return result
```

4. Обновите main.py для обработки нового отчета

```python
# В main.py после чтения данных
if args.report == 'average-rating':
    brand_data = calculate_brand_ratings(products)
elif args.report == 'average-price':
    brand_data = calculate_brand_prices(products)

report_table = generate_report(args.report, brand_data)
```

5. Добавьте тесты для нового отчета

```python

```