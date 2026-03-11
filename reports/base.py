from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Type


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
