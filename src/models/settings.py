from src.dto.settings_dto import SettingsDto
from src.logics.responses.response_format import ResponseFormat
from src.models.abstract_model import AbstractModel
from src.models.company import CompanyModel
from src.models.validators.decorators import validate_setter


######################################
# Модель настроек приложения
class SettingsModel(AbstractModel):
    # соответствующий модели dto класс
    DTO_CLASS = SettingsDto


    _company: CompanyModel = None
    _default_response_format: ResponseFormat = ResponseFormat.JSON
    _first_start: bool = True

    def __init__(self):
        super().__init__()

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

    @staticmethod
    def from_dto(dto: SettingsDto, cache: dict):
        """
            Фабричный метод для создания экземпляра SettingsModel из dto
        """
        item = SettingsModel()
        item.id = dto.id
        item.company = CompanyModel.from_dto(dto.company, cache)
        item.default_response_format = ResponseFormat(dto.default_response_format)
        item.first_start = dto.first_start

        return item

    """
        Перевести доменную модель в DTO
    """
    def to_dto(self) -> SettingsDto:
        return SettingsDto(
            self._id,
            self._company.to_dto(),
            self._default_response_format,
            self._first_start
        )