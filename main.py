import sys

from tabulate import tabulate

from reports.base import ReportFactory
from utils.cli import parse_arguments
from utils.csv_loader import read_csv_files


def main():

    args = parse_arguments()
    data = read_csv_files(args.files)

    if not data:
        print("Ошибка: нет данных для обработки", file=sys.stderr)
        sys.exit(1)

    report = ReportFactory.create(args.report)
    try:
        report_data = report.calculate(data)
    except Exception as e:
        print(f"Ошибка при расчете отчета: {e}", file=sys.stderr)
        sys.exit(1)

    if report_data:
        print(
            tabulate(
                report_data,
                headers=report.headers(),
                tablefmt="grid",
            )
        )
    else:
        print("Нет данных для отображения")


if __name__ == "__main__":
    main()
