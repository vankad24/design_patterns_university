from src.models.validators.exceptions import ArgumentException


def validate_val(value, check_type, check_len=None, check_func=None, none_allowed=False):
    """
    Проверяет значение на корректность.

    Параметры:
    - value: проверяемое значение
    - check_type: тип или кортеж допустимых типов (например, int, str или (int, float))
    - check_len: если указано, проверяется точная длина (len(value) == check_len)
    - check_func: функция проверки, которая возвращает True, если значение корректно
    - none_allowed: если указано False, проверяется, чтобы значение было не None

    Исключения:
    - ArgumentException: вызывается при несоответствии любого из условий

    Примеры использования:
    validate_val("abc", str)                  # проверка типа str
    validate_val("abc", (str, bytes))         # проверка на несколько типов
    validate_val("abc", str, check_len=3)     # проверка длины == 3
    validate_val("123", str, check_func=str.isdigit)  # проверка через функцию
    """

    if not none_allowed and value is None:
        raise ArgumentException("Аргумент со значением None!")

    # Проверка типа
    if value is not None and not isinstance(value, check_type):
        raise ArgumentException(f"Некорректный тип!\nОжидается {check_type}. Текущий тип {type(value)}")

    # Проверка длины
    if check_len is not None and len(value) != check_len:
        raise ArgumentException(f"Некорректная длина аргумента. Ожидалась длина {check_len}, текущая длина {len(value)} для значения `{value}`")

    # Проверка через пользовательскую функцию
    if check_func is not None and not check_func(value):
        raise ArgumentException(f"Аргумент со значением `{value}` не прошёл проверку проверочной функцией")


def not_empty(s: str):
    """
        Возвращает, пустая ли строка без учёта пробелов
    """
    return len(s.strip()) > 0