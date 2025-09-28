def validate_setter(check_type, check_len=None, check_func=None):
    """
    Декоратор для сеттеров, который проверяет тип, длину и/или дополнительную функцию валидации.

    Аргументы:
        check_type: ожидаемый тип значения.
        check_len: необязательная конкретная длина значения.
        check_func: необязательная функция для дополнительной проверки.
    """

    def decorator(setter_func):
        setter_name = setter_func.__name__

        def wrapper(self, value):
            try:
                from src.models.validators.functions import validate_val
                validate_val(value, check_type, check_len, check_func)
            except Exception as e:
                raise RuntimeError(f"Setter '{setter_name}' не выполнился") from e
            setter_func(self, value)

        return wrapper
    return decorator


def func_call(validator_func, *args):
    """
    Декоратор для методов, который вызывает произвольную функцию-валидатор перед установкой значения.

    Аргументы:
        validator_func: функция, которая проверяет значение.
        *args: дополнительные аргументы для функции-валидатора.
    """

    def decorator(func):
        def wrapper(self, value):
            validator_func(value, *args)
            func(self, value)

        return wrapper
    return decorator
