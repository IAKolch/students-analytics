import argparse
import csv
import statistics
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Type

from tabulate import tabulate


class Report(ABC):
    """Базовый класс для всех отчетов."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Имя отчета (используется в командной строке)."""
        pass

    @abstractmethod
    def calculate(self, data: List[Dict[str, Any]]) -> List[Tuple]:
        """
        Расчет данных для отчета.

        Args:
            data: список словарей с данными из CSV

        Returns:
            список кортежей с результатами для вывода
        """
        pass

    @abstractmethod
    def headers(self) -> List[str]:
        """Заголовки колонок для вывода."""
        pass


class MedianCoffeeReport(Report):
    """Отчет о медианных тратах на кофе по студентам."""

    @property
    def name(self) -> str:
        return "median-coffee"

    def calculate(self, data: List[Dict[str, Any]]) -> List[Tuple]:
        """
        Расчет медианных трат на кофе для каждого студента.
        Сортировка по убыванию трат.
        """

        required = {"student", "coffee_spent"}
        if not data:
            return []

        sample = data[0]
        if not required.issubset(sample.keys()):
            missing = required - sample.keys()
            raise ValueError(f"Для отчета {self.name} нужны поля: {missing}")

        spending = defaultdict(list)
        for row in data:
            try:
                student = row["student"]
                coffee = float(row["coffee_spent"])
                spending[student].append(coffee)
            except (ValueError, KeyError) as e:
                print(
                    f"Предупреждение: пропущена некорректная строка: {e}",
                    file=sys.stderr,
                )
                continue

        result = [
            (student, statistics.median(values))
            for student, values in spending.items()
        ]
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def headers(self) -> List[str]:
        return ["student", "median_coffee"]


class ReportFactory:
    """Фабрика для создания отчетов по имени."""

    _reports = {}

    @classmethod
    def register(cls, report_class: Type[Report]) -> None:
        """Регистрация класса отчета."""
        instance = report_class()
        cls._reports[instance.name] = report_class

    @classmethod
    def create(cls, name: str) -> Report:
        """Создание экземпляра отчета по имени."""
        report_class = cls._reports.get(name)
        if not report_class:
            available = ", ".join(cls._reports.keys())
            raise ValueError(
                f"Неизвестный отчет '{name}'. Доступны: {available}"
            )
        return report_class()


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
    parser.add_argument(
        "--report",
        required=True,
        choices=["median-coffee"],
        help="Тип отчета (только median-coffee)",
    )
    return parser.parse_args()


def read_csv_files(file_paths: List[str]) -> List[Dict[str, str]]:
    """
    Чтение данных из нескольких CSV-файлов.

    Args:
        file_paths: список путей к файлам

    Returns:
        список словарей с данными из всех файлов
    """

    all_data = []

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                if not reader.fieldnames:
                    print(
                        f"Предупреждение: файл {file_path} пуст",
                        file=sys.stderr,
                    )
                    continue

                for row in reader:
                    all_data.append(row)

        except FileNotFoundError:
            print(f"Ошибка: файл {file_path} не найден", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}", file=sys.stderr)
            sys.exit(1)

    return all_data


def main():
    """Основная функция."""

    ReportFactory.register(MedianCoffeeReport)
    args = parse_arguments()
    data = read_csv_files(args.files)

    if not data:
        print("Ошибка: нет данных для обработки", file=sys.stderr)
        sys.exit(1)

    try:
        report = ReportFactory.create(args.report)
        report_data = report.calculate(data)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
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
