from types import GenericAlias
from src.core.functions import get_fields, get_type_hints_without_underscore
from src.dto.cached_id import CachedId
from src.dto.measurement_dto import MeasurementUnitDto
from src.models.validators.exceptions import OperationException
from src.models.validators.functions import validate_val

def create_dto(cls, data: dict):
    validate_val(data, dict)
    obj = cls()
    hint_types = get_type_hints_without_underscore(obj.__class__)

    try:
        for key, value in data.items():
            if key in hint_types:
                # Указанный тип в Dto классе
                attr_type = hint_types[key]

                # Проверка list[CachedId]
                if isinstance(attr_type, GenericAlias) and \
                        issubclass(attr_type.__origin__, list) and \
                        issubclass(attr_type.__args__[0], CachedId):
                    arr = [create_dto(CachedId,d) for d in value]
                    setattr(obj, key, arr)
                # Проверка CachedId
                elif isinstance(attr_type, type) and \
                        issubclass(attr_type, CachedId) and isinstance(value, dict):
                    setattr(obj, key, create_dto(CachedId,value))
                else:
                    setattr(obj, key, value)

    except:
        raise OperationException("Невозможно загрузить данные!")

    return obj

