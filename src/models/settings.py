from src.models.company import CompanyModel
from src.models.validators.decorators import validate_setter


######################################
# Модель настроек приложения
class SettingsModel:
    __company: CompanyModel = None

    # Организация
    @property
    def company(self) -> CompanyModel:
        return self.__company

    @company.setter
    @validate_setter(CompanyModel)
    def company(self, value: CompanyModel):
        self.__company = value

