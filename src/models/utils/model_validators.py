from src.models.company import CompanyModel


def validate_str(value: str, length: int, field: str, digits_only: bool = False) -> str:
    value = value.strip()
    if len(value) != length:
        raise ValueError(f"{field} должен содержать ровно {length} символов")
    if digits_only and not value.isdigit():
        raise ValueError(f"{field} должен содержать только цифры")
    return value

def validate_company(company: CompanyModel):
    if not company.name.strip():
        raise ValueError("Наименование не может быть пустым")
    validate_str(company.inn, 12, "ИНН", True)
    validate_str(company.account, 11, "Счет", True)
    validate_str(company.corr_account, 11, "Корреспондентский счет", True)
    validate_str(company.bik, 9, "БИК", True)
    validate_str(company.ownership, 5, "Вид собственности")

