from src.core.observer.event_models import DeleteModelEvent
from src.dto.product_group_dto import ProductGroupDto
from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.exceptions import OperationException
from src.models.validators.functions import not_empty


###############################################
# Модель группы номенклатуры
class ProductGroupModel(AbstractModel):
    def __init__(self):
        super().__init__()

    # соответствующий модели dto класс
    DTO_CLASS = ProductGroupDto

    # Наименование группы
    _name: str = ""

    # --- Название группы ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self._name = value.strip()

    @staticmethod
    def create(name: str):
        """
        Фабричный метод для создания экземпляра ProductGroupModel
        :param name: наименование группы
        :return: экземпляр ProductGroupModel
        """
        item = ProductGroupModel()
        item.name = name
        return item

    @staticmethod
    def from_dto(dto: ProductGroupDto, cache: dict):
        """
            Фабричный метод для создания экземпляра ProductGroupModel из dto
        """
        item = ProductGroupModel()
        item.id = dto.id
        item.name = dto.name
        return item

    """
    Перевести доменную модель в DTO
    """
    def to_dto(self) -> ProductGroupDto:
        return ProductGroupDto(
            self._id,
            self._name
        )

    def on_delete(self, event: DeleteModelEvent) -> bool:
        """
          Обработчик при удалении модели
        """
        if self == event.model:
            raise OperationException(
                f"Нельзя удалить объект `{event.model}`, он используется в {self}"
            )
        return False
