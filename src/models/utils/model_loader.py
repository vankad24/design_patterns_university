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
            attr_type = hint_types.get(key, None)
            if attr_type and issubclass(attr_type, AbstractModel) and isinstance(value, dict):
                model_id = value['id']
                if model_id in created_models:
                    model_obj = created_models.get(model_id, )
                else:
                    model_obj = attr_type.__call__()
                    created_models[model_id] = model_obj
                    load_from_dict(model_obj,value,created_models)
                setattr(obj, key, model_obj)
            else:
                setattr(obj, key, value)
    return created_models