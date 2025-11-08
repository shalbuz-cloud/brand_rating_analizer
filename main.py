"""
Основной скрипт для анализа рейтингов брендов.
"""

import argparse

from core.analyzer import BrandRatingAnalyzer
from core.debug import debug_print, error_print, set_debug_mode


def main() -> int:
    """
    Главная функция скрипта.
    Обрабатывает аргументы командной строки и запускает процесс формирования отчета.
    """
    parser = argparse.ArgumentParser(
        description="Анализ рейтингов брендов из CSV файлов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Примеры использования:
            python main.py --files products1.csv products2.csv --report average-rating
            python main.py -f data/*.csv -r average-rating
            python main.py --list-reports
        """,
    )

    analyzer = BrandRatingAnalyzer()

    # Основная mutually exclusive группа
    main_group = parser.add_mutually_exclusive_group()

    main_group.add_argument(
        "--list-reports", action="store_true", help="Показать доступные отчеты"
    )

    # Группа аргументов для анализа (требуется, если не --list-reports)
    analysis_group = parser.add_argument_group("аргументы анализа")
    analysis_group.add_argument(
        "--files", "-f", nargs="+", help="Пути к CSV файлам с данными о продуктах"
    )

    analysis_group.add_argument(
        "--report",
        "-r",
        choices=analyzer.get_available_reports(),
        help="Тип отчета для генерации",
    )

    # Общие аргументы (доступны всегда)
    parser.add_argument(
        "--debug", action="store_true", help="Включить подробный вывод для отладки"
    )

    args = parser.parse_args()

    if args.list_reports:
        print("Доступные отчеты:")
        for report in analyzer.get_available_reports():
            print("  - %s" % report)
        return 0

    if not args.files or not args.report:
        parser.error(
            "для анализа требуются --files и --report (или используйте --list-reports)"
        )

    # Устанавливаем debug режим для всех модулей
    set_debug_mode(args.debug)

    try:
        # Генерируем и выводим отчет
        debug_print("Чтение файлов: %s" % ", ".join(args.files))
        result = analyzer.analyze(args.files, args.report)

        debug_print("\nОтчет: %s" % args.report)
        debug_print("=" * 40)

        print(result)

    except FileNotFoundError as e:
        error_print("Ошибка: файл не найден - %s" % e)
        return 1

    except Exception as e:
        error_print("Ошибка при выполнении скрипта: %s" % e)
        if args.debug:
            import traceback

            debug_print("Подробности ошибки:\n%s" % traceback.format_exc())
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
