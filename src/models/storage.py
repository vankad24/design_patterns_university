
from src.models.abstract_model import AbstractModel


class StorageModel(AbstractModel):
    __name: str = ""


    # --- Наименование ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Наименование не может быть пустым")
        self.__name = value.strip()

