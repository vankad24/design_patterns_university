from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import not_empty, validate_val


###############################################
# Модель единицы измерения
class MeasurementUnitModel(AbstractModel):
    # Наименование единицы измерения
    __name: str = ""
    # Базовая единица измерения
    __base_unit: "MeasurementUnitModel" = None
    # Коэффициент пересчета к базовой единице
    __conversion_factor: float = 1.0

    def __init__(self, name: str="unknown", conversion_factor: float = 1.0, base_unit: "MeasurementUnitModel" = None):
        """
        Конструктор MeasurementUnitModel
        :param name: название единицы измерения
        :param conversion_factor: коэффициент пересчета к базовой единице
        :param base_unit: ссылка на базовую единицу измерения
        """
        super().__init__()
        self.name = name
        self.conversion_factor = conversion_factor
        self.base_unit = base_unit if base_unit else self

    # --- Название ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self.__name = value.strip()

    # --- Базовая единица ---
    @property
    def base_unit(self) -> "MeasurementUnitModel":
        return self.__base_unit

    @base_unit.setter
    def base_unit(self, value: "MeasurementUnitModel"):
        validate_val(value, MeasurementUnitModel)
        self.__base_unit = value

    # --- Коэффициент пересчета ---
    @property
    def conversion_factor(self) -> float:
        return self.__conversion_factor

    @conversion_factor.setter
    @validate_setter(float)
    def conversion_factor(self, value: float):
        self.__conversion_factor = value

    def convert_to(self, value: float, target_unit: "MeasurementUnitModel") -> float:
        """
        Перевод значения из текущей единицы измерения в целевую единицу.
        """
        if self == target_unit:
            return value
        return self.base_unit.convert_to(value*self.conversion_factor, target_unit)

    @staticmethod
    def create_gram():
        return MeasurementUnitModel.create("грамм")

    @staticmethod
    def create_kg():
        return MeasurementUnitModel.create("кг", MeasurementUnitModel.create_gram(), 1000.0)

    @staticmethod
    def create(name, base=None, factor=1.0):
        validate_val(name,str)
        validate_val(factor,float)

        item = MeasurementUnitModel()
        if base is not None:
            validate_val(base, MeasurementUnitModel)
            item.base_unit = base

        item.name = name
        item.conversion_factor = factor
        return item

