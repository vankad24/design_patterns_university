from src.models.validators.exceptions import ArgumentException


def validate_val(value, check_type, check_len=None, check_func=None):
    """
    Проверяет значение на корректность.

    Параметры:
    - value: проверяемое значение
    - check_type: тип или кортеж допустимых типов (например, int, str или (int, float))
    - check_len: если указано, проверяется точная длина (len(value) == check_len)
    - check_func: функция проверки, которая возвращает True, если значение корректно

    Исключения:
    - ArgumentException: вызывается при несоответствии любого из условий

    Примеры использования:
    validate_val("abc", str)                  # проверка типа str
    validate_val("abc", (str, bytes))         # проверка на несколько типов
    validate_val("abc", str, check_len=3)     # проверка длины == 3
    validate_val("123", str, check_func=str.isdigit)  # проверка через функцию
    """

    if value is None:
        raise ArgumentException("Пустой аргумент")

    # Проверка типа
    if not isinstance(value, check_type):
        raise ArgumentException(f"Некорректный тип!\nОжидается {check_type}. Текущий тип {type(value)}")

    # Проверка длины
    if check_len is not None and len(value) != check_len:
        raise ArgumentException("Некорректная длина аргумента")

    # Проверка через пользовательскую функцию
    if check_func is not None and not check_func(value):
        raise ArgumentException(f"Аргумент со значением `{value}` не прошёл проверку проверочной функцией")


def not_empty(s: str):
    """
        Возвращает, пустая ли строка без учёта пробелов
    """
    return len(s.strip()) > 0