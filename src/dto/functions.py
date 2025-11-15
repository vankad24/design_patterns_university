import json
from types import GenericAlias

from src.core.functions import get_type_hints_without_underscore
from src.dto.abstract_dto import AbstractDto
from src.models.validators.exceptions import OperationException
from src.models.validators.functions import validate_val


def create_dto(dto_class, data: dict):
    """
        Создает экземпляр объекта передачи данных (DTO) заданного класса
        и заполняет его поля данными из словаря.

        Поддерживает рекурсивное создание вложенных DTO (как одиночных, так и в списках).

        :param dto_class: Класс DTO, который нужно создать (должен наследоваться от AbstractDto).
        :param data: Словарь, содержащий данные для инициализации полей DTO.
        :return: Инициализированный экземпляр dto_class.
        :raises OperationException: В случае ошибки при загрузке или валидации данных.
    """
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

def create_from_json(dto_class, json_str: str):
    """
    Создает экземпляр объекта передачи данных (DTO) заданного класса и заполняет его поля данными из json строки.

    :param json_str: Строка json
    :param dto_class: Класс DTO, который нужно создать (должен наследоваться от AbstractDto).
    :return:
    """
    return create_dto(dto_class, json.loads(json_str))
