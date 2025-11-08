"""
Общие фикстуры для всех тестов.
"""

import os
import tempfile

import pytest


@pytest.fixture
def temp_csv_file():
    """
    Фикстура для создания временного CSV файла.
    Автоматически удаляет файл после теста.
    """
    temp_files = []

    def _create_temp_csv(content: str, suffix: str = ".csv") -> str:
        """Создает временный CSV файл с заданным содержимым."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_file = f.name
            temp_files.append(temp_file)
        return temp_file

    yield _create_temp_csv

    # Cleanup - удаляем все созданные временные файлы
    for file in temp_files:
        if os.path.exists(file):
            os.unlink(file)
