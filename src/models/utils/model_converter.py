from src.models.company import CompanyModel


# Конвертация словаря в объект CompanyModel
def dict_to_company(data: dict, to_company_obj=None) -> CompanyModel:
    if to_company_obj is None:
        company = CompanyModel()
    else:
        company = to_company_obj
    if "name" in data:
        company.name = data["name"]
    if "inn" in data:
        company.inn = data["inn"]
    if "account" in data:
        company.account = data["account"]
    if "corr_account" in data:
        company.corr_account = data["corr_account"]
    if "bik" in data:
        company.bik = data["bik"]
    if "ownership" in data:
        company.ownership = data["ownership"]
    return company