from src.logics.responses.response_format import ResponseFormat
from src.models.company import CompanyModel
from src.models.validators.decorators import validate_setter


######################################
# Модель настроек приложения
class SettingsModel:
    _company: CompanyModel = None
    _default_response_format: ResponseFormat = ResponseFormat.JSON
    _first_start: bool = True

    # Организация
    @property
    def company(self) -> CompanyModel:
        return self._company

    @company.setter
    @validate_setter(CompanyModel)
    def company(self, value: CompanyModel):
        self._company = value

    # Формат по умолчанию
    @property
    def default_response_format(self) -> ResponseFormat:
        return self._default_response_format

    @default_response_format.setter
    @validate_setter(ResponseFormat)
    def default_response_format(self, value: ResponseFormat):
        self._default_response_format = value

    # Первый запуск
    @property
    def first_start(self) -> bool:
        return self._first_start

    @first_start.setter
    @validate_setter(bool)
    def first_start(self, value: bool):
        self._first_start = value