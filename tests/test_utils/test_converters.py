"""
Тесты для утилит преобразования данных.
"""

import pytest

from core.utils.converters import safe_strip, safe_float


class TestSafeStrip:
    """Тесты для функции safe_strip."""

    def test_none_value(self):
        """Тест с None значением."""
        assert safe_strip(None) == ""

    def test_empty_string(self):
        """Тест с пустой строкой."""
        assert safe_strip('') == ""

    def test_whitespace_string(self):
        """Тест со строкой из пробелов."""
        assert safe_strip('    ') == ""
        assert safe_strip('\t\n') == ""
        assert safe_strip('   \t\n  ') == ""

    def test_normal_string(self):
        """Тест с нормальной строкой."""
        assert safe_strip('abc') == "abc"

    def test_string_with_spaces(self):
        """Тест со строкой с пробелами вокруг."""
        assert safe_strip(' abc') == "abc"
        assert safe_strip('abc  ') == "abc"
        assert safe_strip(' abc  ') == "abc"

    def test_integer_value(self):
        """Тест с целым числом."""
        assert safe_strip(1234) == "1234"
        assert safe_strip(0) == "0"
        assert safe_strip(-42) == "-42"

    def test_float_value(self):
        """Тест с числом с плавающей точкой."""
        assert safe_strip(3.14) == "3.14"
        assert safe_strip(-2.5) == "-2.5"

    def test_boolean_value(self):
        """Тест с булевым значением."""
        assert safe_strip(True) == "True"
        assert safe_strip(False) == "False"

    def test_list_value(self):
        """Тест со списком."""
        assert safe_strip([1, 2, 3]) == "[1, 2, 3]"

    def test_dict_value(self):
        """Тест со словарем."""
        assert safe_strip({"key": "value"}) == "{'key': 'value'}"

    def test_mixed_whitespace(self):
        """Тест со смешанными пробельными символами."""
        assert safe_strip('  \tabc\t\n') == "abc"
        assert safe_strip('\tabc\n') == "abc"
        assert safe_strip('  \tabc\n') == "abc"


class TestSafeFloat:
    """Тесты для функции safe_float."""

    def test_valid_strings(self):
        """Тест с корректными строковыми значениями."""
        test_cases = [
            ("0", 0.0),
            ("1", 1.0),
            ("3.14", 3.14),
            ("-2.5", -2.5),
            ("  2.7", 2.7),
            ("0.0001", 0.0001),
            ("999.99", 999.99),
        ]

        for input_val, expected in test_cases:
            assert safe_float(input_val) == expected

    def test_numeric_types(self):
        """Тест с числовыми типами."""
        assert safe_float(42) == 42.0
        assert safe_float(3.14) == 3.14
        assert safe_float(0) == 0.0
        assert safe_float(-10) == -10.0

    def test_none_value(self):
        """Тест с None значением."""
        with pytest.raises(ValueError, match='Значение не может быть None'):
            safe_float(None)

    def test_empty_string(self):
        """Тест с пустой строкой."""
        with pytest.raises(ValueError, match='Значение не может быть пустой строкой'):
            safe_float('')

    def test_whitespace_string(self):
        """Тест со строкой только из пробелов."""
        with pytest.raises(ValueError, match='Значение не может быть пустой строкой'):
            safe_float('   ')
        with pytest.raises(ValueError, match='Значение не может быть пустой строкой'):
            safe_float('\t\n')

    def test_invalid_strings(self):
        """Тест с некорректными строковыми значениями."""
        invalid_cases = [
            "hello",
            "12a.34",
            "3.14.15",
            "1,000",  # запятая вместо точки
            "abc123",
            "3.14f",
        ]

        for invalid_case in invalid_cases:
            with pytest.raises(ValueError, match='Невозможно преобразовать'):
                safe_float(invalid_case)

    def test_boolean_value(self):
        """Тест с булевыми значениями."""
        # Булевы значения должны преобразовываться в 1.0 и 0.0
        assert safe_float(True) == 1.0
        assert safe_float(False) == 0.0

    def test_scientific_notation(self):
        """Тест с научной нотацией."""
        assert safe_float('1e10') == 1e10
        assert safe_float('2.5e-3') == 2.5e-3
        assert safe_float('-1.5E+2') == -150.0

    def test_very_small_numbers(self):
        """Тест с очень маленькими числами."""
        assert safe_float('0.0000000001') == 1e-10
        assert safe_float('1e-100') == 1e-100

    def test_very_large_numbers(self):
        """Тест с очень большими числами."""
        assert safe_float('1000000000') == 1000000000.0
        assert safe_float('1e100') == 1e100

    def test_trailing_whitespace(self):
        """Тест с пробелами в начале и конце."""
        assert safe_float('  3.14  ') == 3.14
        assert safe_float('\t2.5\n') == 2.5

    def test_negative_scenarios(self):
        """Тест различных негативных сценариев."""
        # Список нельзя преобразовать в float
        with pytest.raises(ValueError, match='Невозможно преобразовать'):
            safe_float([1, 2, 3])

        # Словарь нельзя преобразовать в float
        with pytest.raises(ValueError, match='Невозможно преобразовать'):
            safe_float({"key": "value"})
