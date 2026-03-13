from reports.median_coffe import MedianCoffeeReport
from utils.csv_loader import read_csv_files


class TestMedianCoffeeReport:

    def test_calculate_with_file(self, temp_csv_file):
        """Тест расчета отчета из файла"""

        report = MedianCoffeeReport()
        data = read_csv_files([temp_csv_file])
        result = report.calculate(data)

        assert len(result) == 2
        result_dict = dict(result)
        assert result_dict["Иван"] == 225.25
        assert result_dict["Мария"] == 200.00

    def test_calculate_with_multiple_files(self, multiple_csv_files):
        """Тест с несколькими файлами"""

        report = MedianCoffeeReport()
        data = read_csv_files(multiple_csv_files)
        result = report.calculate(data)
        students = {item[0] for item in result}
        assert students == {"Иван", "Мария", "Анна", "Петр"}

    def test_calculate_with_dict_data(self, sample_data_dict):
        """Тест расчета с данными из словаря"""

        report = MedianCoffeeReport()
        result = report.calculate(sample_data_dict)
        assert len(result) == 4
        assert result[0][1] >= result[1][1] >= result[2][1] >= result[3][1]

    def test_median_calculation(self, student_with_multiple_entries):
        """Тест правильности вычисления медианы"""

        report = MedianCoffeeReport()
        result = report.calculate(student_with_multiple_entries)
        assert len(result) == 1
        assert result[0][0] == "Иван"
        assert result[0][1] == 187.625

    def test_empty_data(self):
        """Тест с пустыми данными"""

        report = MedianCoffeeReport()
        result = report.calculate([])
        assert result == []
