import argparse

from core.reader import read_product_files
from core.calculator import calculate_brand_ratings
from core.reporter import generate_report


def main() -> int:
    """
    Главная функция скрипта.
    Обрабатывает аргументы командной строки и запускает процесс формирования отчета.
    """
    parser = argparse.ArgumentParser(
        description='Анализ рейтингов брендов из CSV файлов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        Примеры использования:
            python main.py --files products1.csv products2.csv --report average-rating
            python main.py -f data/*.csv -r average-rating
        '''
    )

    # Добавляем аргументы
    parser.add_argument(
        # '--files', '-f',
        '--files',
        nargs='+',  # Принимает один или несколько файлов
        required=True,
        help='Пути к CSV файлам с данными о продуктах'
    )

    parser.add_argument(
        '--report',
        choices=['average-rating'],  # Пока только один тип отчета, но легко расширяемо
        required=True,
        help='Тип отчета для генерации (пока доступен только average-rating)'
    )

    # Парсим аргументы
    args = parser.parse_args()

    try:
        # Читаем данные из всех переданных файлов
        print('Чтение файлов %s' % ", ".join(args.files))
        products = read_product_files(args.files)
        print('Прочитано %d записей о продуктах' % len(products))

        # Вычисляем средние рейтинги по брендам
        brand_ratings = calculate_brand_ratings(products)
        print('Обработано %d брендов' % len(brand_ratings))

        # Генерируем и выводим отчет
        print('\nОтчет: %s' % args.report)  # TODO: генерация вывода отчета через библиотеку "tabulate"
        print('=' * 40)
        report_table = generate_report(args.report, brand_ratings)
        print(report_table)

    except FileNotFoundError as e:
        print('Ошибка: файл не найден - %s' % e)
        return 1

    except Exception as e:
        print('Ошибка при выполнении скрипта: %s' % e)
        return 1

    return 0


if __name__ == '__main__':
    exit(main())  # TODO: Для чего тут exit(main)
