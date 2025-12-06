
from src.dto.cached_id import CachedId
from src.dto.product_remain_dto import ProductRemainDto
from src.models.abstract_model import AbstractModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.storage import StorageModel
from src.models.validators.decorators import validate_setter

# Модель остатков конкретной номенклатуры
class ProductRemainModel(AbstractModel):
    # соответствующий модели dto класс
    DTO_CLASS = ProductRemainDto

    _value: float = 0.0
    _unit: MeasurementUnitModel = None
    _product: ProductModel = None
    _storage: StorageModel = None

    def __init__(self):
        super().__init__()


    # --- Значение (Сумма) ---
    @property
    def value(self) -> float:
        return self._value

    @value.setter
    @validate_setter(float)
    def value(self, value: float):
        self._value = value

    # --- Единица измерения (Unit) ---
    @property
    def unit(self) -> MeasurementUnitModel:
        return self._unit

    @unit.setter
    @validate_setter(MeasurementUnitModel)
    def unit(self, value: MeasurementUnitModel):
        self._unit = value

    # --- Продукт (Product) ---
    @property
    def product(self) -> ProductModel:
        return self._product

    @product.setter
    @validate_setter(ProductModel)
    def product(self, value: ProductModel):
        self._product = value

    # --- Хранилище (Storage) ---
    @property
    def storage(self) -> StorageModel:
        return self._storage

    @storage.setter
    @validate_setter(StorageModel, none_allowed=True)
    def storage(self, value: StorageModel):
        self._storage = value

    # --- Фабричные методы и DTO ---
    @staticmethod
    def create(value: float, unit_model: MeasurementUnitModel,
               product_model: ProductModel, storage_model: StorageModel) -> "ProductRemainModel":
        """
            Фабричный метод для создания экземпляра из dto
        """
        item = ProductRemainModel()
        item.value = value
        item.unit = unit_model
        item.product = product_model
        item.storage = storage_model
        return item

    @staticmethod
    def from_dto(dto: ProductRemainDto, cache: dict) -> "ProductRemainModel":
        item = ProductRemainModel()
        item.id = dto.id
        item.value = dto.value

        if dto.unit is not None:
            item.unit = cache[dto.unit.id]
        if dto.product is not None:
            item.product = cache[dto.product.id]
        if dto.storage is not None:
            item.storage = cache[dto.storage.id]

        return item

    """
    Перевести доменную модель в DTO
    """
    def to_dto(self) -> ProductRemainDto:
        return ProductRemainDto(
            self._id,
            self._value,
            self._unit and CachedId(self._unit.id),
            self._product and CachedId(self._product.id),
            self._storage and CachedId(self._storage.id)
        )




