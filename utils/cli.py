import argparse
from reports.base import ReportFactory


def parse_arguments():
    """Парсинг аргументов командной строки."""

    parser = argparse.ArgumentParser(
        description="Анализ данных о подготовке студентов к экзаменам"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Список CSV-файлов для обработки",
    )
    available_reports = list(ReportFactory._reports.keys())
    parser.add_argument(
        "--report",
        required=True,
        choices=available_reports,
        help="Тип отчета. Доступные: " + ", ".join(available_reports),
    )

    return parser.parse_args()
