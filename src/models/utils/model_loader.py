from src.core.functions import get_type_hints_without_underscore
from src.models.abstract_model import AbstractModel
from src.models.validators.functions import validate_val


def load_from_dict(obj: AbstractModel, data: dict, created_models=None):
    """
    Загружает данные из словаря в атрибуты объекта.
    Игнорирует ключи, начинающиеся с '_', и отсутствующие атрибуты.
    """
    if created_models is None:
        created_models = {}
    validate_val(data, dict)
    validate_val(created_models, dict)
    hint_types = get_type_hints_without_underscore(obj.__class__)
    for key, value in data.items():
        if not key.startswith("_") and hasattr(obj, key):
            # класс поля взятый из type hint
            attr_type = hint_types.get(key, None)
            # если поле является потомком AbstractModel и при этом в него загружается словарь
            if attr_type and issubclass(attr_type, AbstractModel) and isinstance(value, dict):
                # в этом словаре обязательно должен быть id, который должен присутствовать в созданных объектах
                model_obj = created_models[value['id']]
                setattr(obj, key, model_obj)
            else:
                setattr(obj, key, value)
    return created_models