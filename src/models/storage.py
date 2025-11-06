from src.dto.storage_dto import StorageDto
from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import not_empty


###############################################
# Модель склада
class StorageModel(AbstractModel):
    # соответствующий модели dto класс
    DTO_CLASS = StorageDto

    # Наименование склада
    _name: str = ""
    # Адрес склада
    _address: str = ""

    # --- Название склада ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self._name = value.strip()

    # --- Адрес склада ---
    @property
    def address(self) -> str:
        return self._address

    @address.setter
    @validate_setter(str, check_func=not_empty)
    def address(self, value: str):
        self._address = value.strip()

    @staticmethod
    def from_dto(dto: StorageDto, cache: dict):
        """
            Фабричный метод для создания экземпляра StorageModel из dto
        """
        item = StorageModel()
        item.id = dto.id
        item.name = dto.name
        item.address = dto.address
        return item

    """
    Перевести доменную модель в DTO
    """
    def to_dto(self) -> StorageDto:
        return StorageDto(
            self._id,
            self._name,
            self._address
        )
