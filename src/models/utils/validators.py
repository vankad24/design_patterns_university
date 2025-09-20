

def validate_str(value: str, length: int, field: str, digits_only: bool = False) -> str:
    value = value.strip()
    if len(value) != length:
        raise ValueError(f"{field} должен содержать ровно {length} символов")
    if digits_only and not value.isdigit():
        raise ValueError(f"{field} должен содержать только цифры")
    return value
