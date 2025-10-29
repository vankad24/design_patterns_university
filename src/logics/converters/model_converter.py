from src.core.functions import get_fields
from src.logics.converters.abstract_converter import AbstractConverter
from src.models.abstract_model import AbstractModel

"""Конвертер моделей"""
class ModelConverter(AbstractConverter):

    """Переопределённый метод convert"""
    def convert(self, obj) -> dict:

        result = dict()
        fields = get_fields(obj)
        for field in fields:
            value = getattr(obj, field)
            if isinstance(value, AbstractModel):
                result[field] = self.convert(value)
            else:
                from src.logics.factory_converters import FactoryConverters
                result[field] = FactoryConverters.convert(value)

        return result
