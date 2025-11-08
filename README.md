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

# Показать доступные отчеты
python main.py --list-reports

# Запустить анализ
python main.py --files products1.csv products2.csv --report average-rating

# Сокращенная версия
python main.py -f products.csv -r average-rating

# С debug
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

## Разработка

```bash
# Установка dev-зависимостей
make install

# Запуск линтера (ruff)
make lint

# Форматирование кода (black)
make format

# Проверка типов (mypy)
make type-check

# Запуск тестов
make test

# Тесты с покрытием
make test-cov

# Все проверки сразу (lint + type-check + test)
make check

# Очистка временных файлов
make clean

# Полная установка и проверка
make dev

# Показать все команды
make help
```

## Добавление новых отчетов

Архитектура проекта позволяет легко добавлять новые типы отчетов.

```text
core/reports/
├── init.py
├── base.py  # Фабрика отчетов (ReportFactory)
└── (ваш_отчет).py # Новый класс отчета
```

#### 1. Создайте новый класс отчета

Создайте новый файл в папке `core/reports/` или добавьте класс в существующий файл:

```python
from core.reports import Report
from core.models import BrandStatistics
from tabulate import tabulate


class AveragePriceReport(Report):
    """
    Отчет по средним ценам по брендам.
    Реализует паттерн Strategy для генерации отчетов.
    """

    @property
    def name(self) -> str:
        """Уникальный идентификатор отчета."""
        return "average-price"

    def generate(self, data: list[BrandStatistics]) -> str:
        """
        Генерирует табличный отчет со средними ценами.
        
        :param data: Статистические данные по брендам
        :return: Отформатированная таблица в виде строки
        """
        table_data = []
        for index, stats in enumerate(data, start=1):
            table_data.append([
                index,
                stats.brand,
                f"${stats.average_price:.2f}",  # Форматирование цены
            ])

        return tabulate(
            table_data,
            headers=['', 'brand', 'average_price'],
            tablefmt='grid',
            stralign='center',
            numalign='center',
        )
```

#### 2. Зарегистрируйте отчет в фабрике

Добавьте регистрацию в `core/reports/base.py`:

```python
from .base import Report, ReportFactory
from .average_rating import AverageRatingReport
from .average_price import AveragePriceReport

# Регистрируем отчеты
ReportFactory.register('average-rating', AverageRatingReport)
ReportFactory.register('average-price', AveragePriceReport)

# Для обратной совместимости
__all__ = ['Report', 'ReportFactory', 'AverageRatingReport', 'AveragePriceReport']
```

#### 3. Добавьте новый калькулятор статистик (если нужно)

Если для отчета нужны новые метрики, создайте калькулятор в `core/calculator.py`:

```python
class BrandPriceCalculator(StatisticsCalculator):
    """
    Калькулятор средних цен по брендам.
    Наследует абстрактный класс StatisticsCalculator.
    """
    
    def calculate(self, products: List[Product]) -> List[BrandStatistics]:
        """Вычисляет средние цены для всех брендов."""
        if not products:
            return []
        
        brand_stats = defaultdict(lambda: {"total_price": 0, "count": 0})
        
        for product in products:
            brand_stats[product.brand]["total_price"] += product.price
            brand_stats[product.brand]["count"] += 1
        
        statistics = []
        for brand, stats in brand_stats.items():
            avg_price = stats["total_price"] / stats["count"]
            statistics.append(BrandStatistics(
                brand=brand,
                average_price=round(avg_price, 2),  # Новая метрика
                product_count=stats["count"]
            ))
        
        return sorted(statistics, key=lambda x: x.average_price, reverse=True)
```

#### 4. Обновите модель BrandStatistics (если нужно)

Добавьте новые поля в `core/models.py`:

```python
@dataclass
class BrandStatistics:
    """DTO для статистики бренда с расширенными метриками."""
    
    brand: str
    average_rating: float = None
    average_price: float = None        # Новая метрика
    product_count: int = None
    
    def __post_init__(self):
        """Округляет числовые значения."""
        if self.average_rating is not None:
            self.average_rating = round(self.average_rating, 2)
        if self.average_price is not None:
            self.average_price = round(self.average_price, 2)
```

#### 5. Обновите Analyzer для поддержки нового отчета

Модифицируйте `core/analyzer.py`:

```python
class BrandRatingAnalyzer:
    """Фасад для анализа данных с поддержкой различных отчетов."""
    
    def __init__(self):
        self.reader = CSVProductReader(DataValidator(), DataConverter())
        self.rating_calculator = BrandRatingCalculator()
        self.price_calculator = BrandPriceCalculator()  # Новый калькулятор
    
    def analyze(self, file_paths: List[str], report_type: str) -> str:
        """Выполняет анализ и генерирует указанный отчет."""
        products = self.reader.read(file_paths)
        
        # Выбираем калькулятор в зависимости от типа отчета
        if report_type == "average-rating":
            statistics = self.rating_calculator.calculate(products)
        elif report_type == "average-price":
            statistics = self.price_calculator.calculate(products)
        else:
            statistics = self.rating_calculator.calculate(products)
        
        report = ReportFactory.create(report_type)
        return report.generate(statistics)
```

#### 6. Использование нового отчета

После добавления отчет автоматически становится доступен:

```bash
# Просмотр доступных отчетов
python main.py --list-reports
# Вывод:
#   - average-rating
#   - average-price

# Использование нового отчета
python main.py --files products.csv --report average-price
```