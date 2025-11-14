from src.dto.cached_id import CachedId
from src.dto.tbs_dto import TurnoverBalanceItemDto
from src.models.abstract_model import AbstractModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.storage import StorageModel
from src.models.validators.decorators import validate_setter


class TurnoverBalanceItem(AbstractModel):
    def __init__(self):
        super().__init__()

    # соответствующий модели dto класс
    DTO_CLASS = TurnoverBalanceItemDto

    # --- Приватные поля ---
    _storage: StorageModel = None
    _product: ProductModel = None
    _unit: MeasurementUnitModel = None
    _start_balance: float = 0.0
    _inflows: float = 0.0
    _outflows: float = 0.0

    # --- Склад (Storage) ---
    @property
    def storage(self) -> StorageModel:
        return self._storage

    @storage.setter
    @validate_setter(StorageModel, none_allowed=True)
    def storage(self, value: StorageModel):
        self._storage = value

    # --- Продукт (Product) ---
    @property
    def product(self) -> ProductModel:
        return self._product

    @product.setter
    @validate_setter(ProductModel)
    def product(self, value: ProductModel):
        self._product = value

    # --- Единица измерения (Unit) ---
    @property
    def unit(self) -> MeasurementUnitModel:
        return self._unit

    @unit.setter
    @validate_setter(MeasurementUnitModel)
    def unit(self, value: MeasurementUnitModel):
        self._unit = value

    # --- Начальное сальдо (Start Balance) ---
    @property
    def start_balance(self) -> float:
        return self._start_balance

    @start_balance.setter
    @validate_setter(float)
    def start_balance(self, value: float):
        self._start_balance = value

    # --- Поступления (Inflows) ---
    @property
    def inflows(self) -> float:
        return self._inflows

    @inflows.setter
    @validate_setter(float)
    def inflows(self, value: float):
        self._inflows = value

    # --- Расходы (Outflows) ---
    @property
    def outflows(self) -> float:
        return self._outflows

    @outflows.setter
    @validate_setter(float, check_func=lambda x: x <= 0) # Расходы обычно отрицательны или нулевые
    def outflows(self, value: float):
        self._outflows = value

    # --- Вычисляемые свойства (Computed Properties) ---

    @property
    def change_in_balance(self) -> float:
        """Изменение за период: поступления + расходы (расходы < 0)"""
        return self.inflows + self.outflows

    @property
    def end_balance(self) -> float:
        """Конечное сальдо"""
        return self.start_balance + self.change_in_balance

    # --- Фабричные методы и DTO-методы ---

    @staticmethod
    def create(
        storage: StorageModel|None,
        product: ProductModel,
        unit: MeasurementUnitModel,
        start_balance: float = 0.0,
        inflows: float = 0.0,
        outflows: float = 0.0
    ) -> 'TurnoverBalanceItem':
        """
        Фабричный метод для создания экземпляра TurnoverBalanceItem.
        """
        item = TurnoverBalanceItem()
        item.storage = storage
        item.product = product
        item.unit = unit
        item.start_balance = start_balance
        item.inflows = inflows
        item.outflows = outflows
        return item

    @staticmethod
    def from_dto(dto: TurnoverBalanceItemDto, cache: dict) -> 'TurnoverBalanceItem':
        """
            Фабричный метод для создания экземпляра TurnoverBalanceItem из dto
        """
        item = TurnoverBalanceItem()
        item.id = dto.id
        item.start_balance = dto.start_balance
        item.inflows = dto.inflows
        item.outflows = dto.outflows

        # Загрузка вложенных моделей из кеша
        if dto.storage is not None:
            # Предполагается, что CachedId имеет атрибут id, по которому можно получить модель из кеша
            item.storage = cache[dto.storage.id]

        if dto.product is not None:
            item.product = cache[dto.product.id]

        if dto.unit is not None:
            item.unit = cache[dto.unit.id]

        return item

    def to_dto(self) -> TurnoverBalanceItemDto:
        """
        Перевести доменную модель в DTO
        """
        return TurnoverBalanceItemDto(
            id=self._id,
            # Заменяем вложенные модели на CachedId(id)
            storage=self._storage and CachedId(self._storage.id),
            product=self._product and CachedId(self._product.id),
            unit=self._unit and CachedId(self._unit.id),
            start_balance=self._start_balance,
            inflows=self._inflows,
            outflows=self._outflows
        )