"""
    Файл с дополнительными, вспомогательными функциями.
"""
from typing import Optional


def str_to_int(x: str) -> Optional[int]:
    """
        Перевод строки в число.
    """
    try:
        x = int(x)
        return x
    except Exception:
        return None
