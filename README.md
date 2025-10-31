# Brand Rating Analyzer

Скрипт для анализа рейтингов брендов из CSV файлов.

## Установка

1. Клонируйте репозиторий
   ```bash
   git clone git@github.com:shalbuz-cloud/brand_rating_analizer.git
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
   
## Использование
```bash
python main.py --files products1.csv products2.csv --report average-rating
```

## Запуск тестов
```bash
pytest tests/
```

## Формат CSV файлов

CSV файлы должны содержать следующие колонки:

- `name` - название продукта
- `brand` - бренд продукта
- `price` - цена продукта
- `rating` - рейтинг продукта (от 0 до 5)
