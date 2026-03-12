import csv
import os
import tempfile

import pytest


@pytest.fixture
def temp_csv_file():
    """Создает временный CSV файл с валидными тестовыми данными"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                    encoding='utf-8', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=['student', 'date', 'coffee_spent', 
                                              'sleep_hours', 'study_hours', 'mood', 'exam'])
        writer.writeheader()
        writer.writerows([
            {"student": "Иван", "date": "2024-01-15", "coffee_spent": "150.50",
             "sleep_hours": "7.5", "study_hours": "4.0", "mood": "жив", "exam": "math"},
            {"student": "Мария", "date": "2024-01-15", "coffee_spent": "200.00",
             "sleep_hours": "8.0", "study_hours": "5.0", "mood": "цел", "exam": "physics"},
            {"student": "Иван", "date": "2024-01-16", "coffee_spent": "300.00",
             "sleep_hours": "8.0", "study_hours": "6.0", "mood": "орел", "exam": "math"},
        ])
        temp_path = f.name
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def multiple_csv_files(temp_csv_file):
    """Создает несколько временных CSV файлов"""

    files = [temp_csv_file]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                    encoding='utf-8', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=['student', 'date', 'coffee_spent',
                                              'sleep_hours', 'study_hours', 'mood', 'exam'])
        writer.writeheader()
        writer.writerows([
            {"student": "Анна", "date": "2024-01-16", "coffee_spent": "250.50",
             "sleep_hours": "7.0", "study_hours": "5.5", "mood": "хорошо", "exam": "biology"},
            {"student": "Петр", "date": "2024-01-16", "coffee_spent": "180.00",
             "sleep_hours": "6.5", "study_hours": "4.5", "mood": "нейтрально", "exam": "chemistry"},
        ])
        files.append(f.name)
    
    yield files

    for file in files[1:]:
        if os.path.exists(file):
            os.unlink(file)

@pytest.fixture
def sample_data_dict():
    """Тестовые данные в виде словаря (без создания файла)"""

    return [
        {"student": "Иван", "coffee_spent": "150.50"},
        {"student": "Мария", "coffee_spent": "200.00"},
        {"student": "Иван", "coffee_spent": "300.00"},
        {"student": "Петр", "coffee_spent": "180.00"},
        {"student": "Анна", "coffee_spent": "250.50"},
    ]

@pytest.fixture
def student_with_multiple_entries():
    """Студент с несколькими записями для тестирования медианы"""

    return [
        {"student": "Иван", "coffee_spent": "150.50"},
        {"student": "Иван", "coffee_spent": "200.00"},
        {"student": "Иван", "coffee_spent": "175.25"},
        {"student": "Иван", "coffee_spent": "300.00"},
    ]