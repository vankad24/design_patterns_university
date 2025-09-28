from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import not_empty
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product_group import ProductGroupModel


###############################################
# Модель номенклатуры
class ProductModel(AbstractModel):
    def __init__(self):
        super().__init__()

    # Код номенклатуры
    __code: str = ""
    # Название номенклатуры (до 50 символов)
    __name: str = ""
    # Полное наименование (до 255 символов)
    __full_name: str = ""
    # Единица измерения
    __unit: MeasurementUnitModel = None
    # Группа номенклатуры
    __group: ProductGroupModel = None
    # Цена
    __price: float = 0.0

    # --- Код ---
    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    @validate_setter(str, check_func=not_empty)
    def code(self, value: str):
        self.__code = value.strip()

    # --- Название ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    @validate_setter(str, check_func=lambda x: 0 < len(x.strip()) <= 50)
    def name(self, value: str):
        self.__name = value.strip()

    # --- Полное наименование ---
    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    @validate_setter(str, check_func=lambda x: 0 < len(x.strip()) <= 255)
    def full_name(self, value: str):
        self.__full_name = value.strip()

    # --- Единица измерения ---
    @property
    def unit(self) -> MeasurementUnitModel:
        return self.__unit

    @unit.setter
    @validate_setter(MeasurementUnitModel)
    def unit(self, value: MeasurementUnitModel):
        self.__unit = value

    # --- Группа номенклатуры ---
    @property
    def group(self) -> ProductGroupModel:
        return self.__group

    @group.setter
    @validate_setter(ProductGroupModel)
    def group(self, value: ProductGroupModel):
        self.__group = value

    # --- Цена ---
    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    @validate_setter(float)
    def price(self, value: float):
        self.__price = value
