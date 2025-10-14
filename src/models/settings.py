from src.models.company import CompanyModel
from src.models.validators.decorators import validate_setter


######################################
# Модель настроек приложения
class SettingsModel:
    _company: CompanyModel = None

    # Организация
    @property
    def company(self) -> CompanyModel:
        return self._company

    @company.setter
    @validate_setter(CompanyModel)
    def company(self, value: CompanyModel):
        self._company = value

