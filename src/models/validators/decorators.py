def validate_setter(check_type, check_len=None, check_func=None):
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
    def decorator(setter):
        def wrapper(self, value):
            validator_func(value, *args)
            setter(self, value)
        return wrapper
    return decorator

