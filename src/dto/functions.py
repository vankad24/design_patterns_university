from types import GenericAlias
from src.core.functions import get_fields, get_type_hints_without_underscore
from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId
from src.dto.measurement_dto import MeasurementUnitDto
from src.models.validators.exceptions import OperationException
from src.models.validators.functions import validate_val

def create_dto(dto_class, data: dict):
    validate_val(data, dict)
    obj = dto_class()
    hint_types = get_type_hints_without_underscore(obj.__class__)

    try:
        for key, value in data.items():
            if key in hint_types:
                # Указанный тип в Dto классе
                attr_type = hint_types[key]

                # Проверка list[AbstractDto]
                if isinstance(attr_type, GenericAlias) and \
                        issubclass(attr_type.__origin__, list) and \
                        issubclass(attr_type.__args__[0], AbstractDto):
                    arr = [create_dto(attr_type.__args__[0], d) for d in value]
                    setattr(obj, key, arr)
                # Проверка вложенного AbstractDto
                elif isinstance(attr_type, type) and \
                        issubclass(attr_type, AbstractDto) and isinstance(value, dict):
                    setattr(obj, key, create_dto(attr_type, value))
                else:
                    setattr(obj, key, value)

    except:
        raise OperationException("Невозможно загрузить данные!")

    return obj

