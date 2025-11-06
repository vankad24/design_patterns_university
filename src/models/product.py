from src.dto.cached_id import CachedId
from src.dto.product_dto import ProductDto
from src.models.abstract_model import AbstractModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product_group import ProductGroupModel
from src.models.validators.decorators import validate_setter


###############################################
# Модель номенклатуры
class ProductModel(AbstractModel):
    def __init__(self):
        super().__init__()

    # соответствующий модели dto класс
    DTO_CLASS = ProductDto

    # Название номенклатуры (до 50 символов)
    _name: str = ""
    # Полное наименование (до 255 символов)
    _full_name: str = ""
    # Единица измерения
    _unit: MeasurementUnitModel = None
    # Группа номенклатуры
    _group: ProductGroupModel = None

    # --- Название ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @validate_setter(str, check_func=lambda x: 0 < len(x.strip()) <= 50)
    def name(self, value: str):
        self._name = value.strip()

    # --- Полное наименование ---
    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    @validate_setter(str, check_func=lambda x: 0 < len(x.strip()) <= 255)
    def full_name(self, value: str):
        self._full_name = value.strip()

    # --- Единица измерения ---
    @property
    def unit(self) -> MeasurementUnitModel:
        return self._unit

    @unit.setter
    @validate_setter(MeasurementUnitModel)
    def unit(self, value: MeasurementUnitModel):
        self._unit = value

    # --- Группа номенклатуры ---
    @property
    def group(self) -> ProductGroupModel:
        return self._group

    @group.setter
    @validate_setter(ProductGroupModel)
    def group(self, value: ProductGroupModel):
        self._group = value

    @staticmethod
    def create(name: str, full_name: str = "", unit: MeasurementUnitModel = None, group: "ProductGroupModel" = None):
        """
        Фабричный метод для создания экземпляра ProductModel
        :param name: краткое наименование (до 50 символов)
        :param full_name: полное наименование (до 255 символов)
        :param unit: единица измерения
        :param group: группа номенклатуры
        :return: экземпляр ProductModel
        """
        item = ProductModel()
        item.name = name
        if full_name:
            item.full_name = full_name
        if unit:
            item.unit = unit
        if group:
            item.group = group
        return item

    @staticmethod
    def from_dto(dto: ProductDto, cache: dict):
        """
            Фабричный метод для создания экземпляра ProductModel из dto
        """
        item = ProductModel()
        item.id = dto.id
        item.name = dto.name
        item.full_name = dto.full_name

        if dto.unit is not None:
            item.unit = cache[dto.unit.id]

        if dto.group is not None:
            item.group = cache[dto.group.id]

        return item

    """
    Перевести доменную модель в Dto
    """
    def to_dto(self) -> ProductDto:
        return ProductDto(self._id,
                          self._name,
                          self._full_name,
                          self._unit and CachedId(self._unit.id),
                          self._group and CachedId(self._group.id))

