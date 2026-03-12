import statistics
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from reports.base import Report


class MedianCoffeeReport(Report):
    """Отчет о медианных тратах на кофе по студентам."""

    @property
    def name(self) -> str:
        return "median-coffee"

    def calculate(self, data: List[Dict[str, Any]]) -> List[Tuple]:
        valid_data = self._parse(data)
        grouped = self._group_by_student(valid_data)
        result = self._compute_medians(grouped)
        return sorted(result, key=lambda x: x[1], reverse=True)

    def _parse(self, data: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
        """
        Парсит траты на кофе в float.

        Args:
            data: список словарей с данными из CSV

        Returns:
            список кортежей (student, coffee_spent) с валидными данными
        """
        valid_entries = []

        for row in data:
            student = row["student"]
            coffee_spent = float(row["coffee_spent"])
            valid_entries.append((student, coffee_spent))

        return valid_entries

    def _group_by_student(
        self, parsed_data: List[Tuple[str, float]]
    ) -> Dict[str, List[float]]:
        """
        Группирует траты по студентам.

        Args:
            parsed_data: список кортежей (student, coffee_spent)

        Returns:
            словарь: ключ — имя студента, значение — список его трат на кофе
        """
        grouped_data = defaultdict(list)

        for student, coffee_spent in parsed_data:
            grouped_data[student].append(coffee_spent)

        return dict(grouped_data)

    def _compute_medians(
        self, grouped_data: Dict[str, List[float]]
    ) -> List[Tuple[str, float]]:
        """
        Вычисляет медианные траты для каждого студента.

        Args:
            grouped_data: словарь с группировкой трат по студентам

        Returns:
            список кортежей (student, median_coffee)
        """
        median_results = []

        for student, spending_list in grouped_data.items():
            median_value = statistics.median(spending_list)
            median_results.append((student, median_value))

        return median_results

    def headers(self) -> List[str]:
        return ["student", "median_coffee"]
