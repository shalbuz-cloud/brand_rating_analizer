from core.calculator import CalculatorFactory
from core.debug import debug_print, error_print
from core.reader import CSVProductReader
from core.reports import ReportFactory
from core.utils.converters import DataConverter
from core.utils.validators import DataValidator


class BrandRatingAnalyzer:
    """
    Фасад для анализа рейтингов брендов.
    Использует фабрики для создания калькуляторов и отчетов.
    """

    def __init__(self) -> None:
        """
        Инициализирует анализатор с необходимыми компонентами.
        """
        debug_print("Initializing BrandRatingAnalyzer")
        self.reader = CSVProductReader(DataValidator(), DataConverter())
        debug_print("BrandRatingAnalyzer initialized successfully")

    def analyze(self, file_paths: list[str], report_type: str) -> str:
        """
        Выполняет полный анализ: чтение данных, расчет статистик, генерация отчета.
        :param file_paths: Список путей к файлам с данными
        :param report_type: Тип отчета для генерации
        :return: Сгенерированный отчет в виде строки
        """

        debug_print("Starting analysis: files=%s, report=%s", file_paths, report_type)

        try:
            # Чтение данных
            products = self.reader.read(file_paths)

            # Создание калькулятора по типу отчета
            calculator = CalculatorFactory.create(report_type)
            statistics = calculator.calculate(products)

            # Создание отчета
            report = ReportFactory.create(report_type)
            result = report.generate(statistics)

            debug_print("Analysis completed successfully")
            return result

        except Exception as e:
            error_print("Analysis failed: %s", e)
            raise

    @staticmethod
    def get_available_reports() -> list[str]:
        """
        Возвращает список доступных типов отчетов.

        :return: Список идентификаторов отчетов.
        """
        reports = ReportFactory.get_available_reports()
        debug_print("Available reports: %s", reports)
        return reports
