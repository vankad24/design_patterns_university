from src.models.company import CompanyModel


# Конвертация словаря в объект CompanyModel
def dict_to_company(data: dict, to_company_obj=None) -> CompanyModel:
    if not isinstance(data, dict):
        raise ValueError("Для конвертации нужен словарь")
    required_keys = ["name", "inn", "account", "corr_account", "bik", "ownership"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"В словаре нет обязательного значения '{key}'")

    if to_company_obj is None:
        company = CompanyModel()
    else:
        company = to_company_obj

    company.name = data["name"]
    company.inn = data["inn"]
    company.account = data["account"]
    company.corr_account = data["corr_account"]
    company.bik = data["bik"]
    company.ownership = data["ownership"]
    return company