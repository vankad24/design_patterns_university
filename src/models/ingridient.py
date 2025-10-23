from src.dto.ingridient_dto import IngredientDto
from src.models.abstract_model import AbstractModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.validators.decorators import validate_setter


###############################################
# Модель ингредиента рецепта
class IngredientModel(AbstractModel):
    def __init__(self):
        super().__init__()

    # Продукт
    _product: ProductModel = None
    # Количество
    _amount: float = 0.0
    # Единица измерения
    _unit: MeasurementUnitModel = None

    # --- Продукт ---
    @property
    def product(self) -> ProductModel:
        return self._product

    @product.setter
    @validate_setter(ProductModel)
    def product(self, value: ProductModel):
        self._product = value

    # --- Количество ---
    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    @validate_setter(float, check_func=lambda x: x > 0)
    def amount(self, value: float):
        self._amount = value

    # --- Единица измерения ---
    @property
    def unit(self) -> MeasurementUnitModel:
        return self._unit

    @unit.setter
    @validate_setter(MeasurementUnitModel)
    def unit(self, value: MeasurementUnitModel):
        self._unit = value

    @staticmethod
    def create(product: ProductModel, amount: float, unit: MeasurementUnitModel):
        """
        Фабричный метод для создания экземпляра IngredientModel.
        :param product: экземпляр ProductModel
        :param amount: количество (float > 0)
        :param unit: экземпляр MeasurementUnitModel
        :return: экземпляр IngredientModel
        """
        item = IngredientModel()
        item.product = product
        item.amount = amount
        item.unit = unit
        return item

    @staticmethod
    def from_dto(dto: IngredientDto, cache: dict):
        """
            Фабричный метод для создания экземпляра IngredientModel из dto
        """
        item = IngredientModel()
        item.id = dto.id
        item.name = dto.name
        item.amount = dto.amount

        if dto.product is not None:
            item.product = cache[dto.product.id]

        if dto.unit is not None:
            item.unit = cache[dto.unit.id]

        return item