from src.models.company import CompanyModel
from src.models.utils.validators import validate_str


def validate_company(company: CompanyModel):
    if not company.name.strip():
        raise ValueError("Наименование не может быть пустым")
    validate_str(company.inn, 12, "ИНН", True)
    validate_str(company.account, 11, "Счет", True)
    validate_str(company.corr_account, 11, "Корреспондентский счет", True)
    validate_str(company.bik, 9, "БИК", True)
    validate_str(company.ownership, 5, "Вид собственности")

