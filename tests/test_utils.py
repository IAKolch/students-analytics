import pytest

from utils.cli import parse_arguments
from utils.csv_loader import read_csv_files


class TestCliParser:

    def test_parse_arguments_with_files(self, mocker):
        """Тест парсинга аргументов с файлами"""

        mock_args = mocker.MagicMock()
        mock_args.files = ["file1.csv", "file2.csv"]
        mock_args.report = "median-coffee"

        mock_parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
        mock_parse_args.return_value = mock_args

        mocker.patch(
            "reports.base.ReportFactory._reports", {"median-coffee": None}
        )

        args = parse_arguments()

        assert args.files == ["file1.csv", "file2.csv"]
        assert args.report == "median-coffee"

    def test_parse_arguments_single_file(self, mocker):
        """Тест с одним файлом"""

        mock_args = mocker.MagicMock()
        mock_args.files = ["data.csv"]
        mock_args.report = "median-coffee"

        mock_parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
        mock_parse_args.return_value = mock_args

        mocker.patch(
            "reports.base.ReportFactory._reports", {"median-coffee": None}
        )

        args = parse_arguments()

        assert args.files == ["data.csv"]
        assert len(args.files) == 1


class TestCsvLoader:

    def test_read_single_file(self, temp_csv_file):
        """Тест с одним файлом"""

        data = read_csv_files([temp_csv_file])
        assert len(data) == 3
        assert data[0]["student"] == "Иван"
        assert data[0]["coffee_spent"] == "150.50"
        assert data[0]["date"] == "2024-01-15"
        assert data[0]["sleep_hours"] == "7.5"
        assert data[0]["study_hours"] == "4.0"
        assert data[0]["mood"] == "жив"
        assert data[0]["exam"] == "math"

    def test_read_multiple_files(self, multiple_csv_files):
        """Тест с несколькими файлами"""

        data = read_csv_files(multiple_csv_files)
        assert len(data) == 5

    def test_file_not_found(self):
        """Тест с несуществующим файлом"""

        with pytest.raises(SystemExit):
            read_csv_files(["non_existent_file.csv"])

    def test_empty_file(self, temp_csv_file):
        """Тест с пустым файлом"""

        with open(temp_csv_file, "w", encoding="utf-8") as f:
            f.write("")
        data = read_csv_files([temp_csv_file])
        assert data == []
