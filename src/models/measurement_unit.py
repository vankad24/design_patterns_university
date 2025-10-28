from src.dto.measurement_dto import MeasurementUnitDto
from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import not_empty, validate_val


###############################################
# Модель единицы измерения
class MeasurementUnitModel(AbstractModel):
    # Наименование единицы измерения
    _name: str = ""
    # Базовая единица измерения
    _base_unit: "MeasurementUnitModel" = None
    # Коэффициент пересчета к базовой единице
    _conversion_factor: float = 1.0

    def __init__(self):
        super().__init__()

    # --- Название ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self._name = value.strip()

    # --- Базовая единица ---
    @property
    def base_unit(self) -> "MeasurementUnitModel":
        return self._base_unit

    @base_unit.setter
    def base_unit(self, value: "MeasurementUnitModel"):
        validate_val(value, MeasurementUnitModel)
        self._base_unit = value

    # --- Коэффициент пересчета ---
    @property
    def conversion_factor(self) -> float:
        return self._conversion_factor

    @conversion_factor.setter
    @validate_setter(float)
    def conversion_factor(self, value: float):
        self._conversion_factor = value

    def convert_to(self, value: float, target_unit: "MeasurementUnitModel") -> float:
        """
        Перевод значения из текущей единицы измерения в целевую единицу.
        """
        if self == target_unit:
            return value
        return self.base_unit.convert_to(value*self.conversion_factor, target_unit)


    @staticmethod
    def create(name, factor=1.0, base=None):
        """
        Фабричный метод для создания экземпляра класса
        """

        item = MeasurementUnitModel()
        if base is not None:
            item.base_unit = base
        item.name = name
        item.conversion_factor = factor
        return item

    @staticmethod
    def from_dto(dto: MeasurementUnitDto, cache: dict):
        """
            Фабричный метод для создания экземпляра MeasurementDto из dto
        """
        item = MeasurementUnitModel()
        item.id = dto.id
        item.name = dto.name
        if dto.base_unit is not None:
            item.base_unit = cache[dto.base_unit.id]
        item.conversion_factor = dto.conversion_factor
        return item

