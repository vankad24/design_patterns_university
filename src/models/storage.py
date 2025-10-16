from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import not_empty


###############################################
# Модель склада
class StorageModel(AbstractModel):
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
