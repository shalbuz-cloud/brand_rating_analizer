"""
Модуль для управления debug-выводом.
"""

import sys
from typing import Any

# Глобальная переменная для режима отладки
_DEBUG = False


def set_debug_mode(debug: bool) -> None:
    """
    Включает или выключает debug-режим.

    :param debug: True для включения debug-вывода
    """
    global _DEBUG
    _DEBUG = debug


def debug_print(*args: Any, **kwargs: Any) -> None:
    """
    Выводит сообщение только, если включен debug-режим.

    :param args: Аргументы для print
    :param kwargs: Ключевые аргументы для print
    """
    if _DEBUG:
        print(*args, **kwargs)


def error_print(*args: Any, **kwargs: Any) -> None:
    """
    Выводит сообщение об ошибке (всегда, независимо от debug-режима).

    :param args: Аргументы для print
    :param kwargs: Ключевые аргументы для print
    """
    print(*args, **kwargs, file=sys.stderr)
