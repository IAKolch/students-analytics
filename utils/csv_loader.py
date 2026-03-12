import csv
import sys
from typing import Dict, List


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
