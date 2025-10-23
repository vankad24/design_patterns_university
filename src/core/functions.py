import json
from typing import get_type_hints

def load_json(file_name):
    """
    Загружает JSON-данные из файла.

    :param file_name: путь к файлу JSON (строка). Пробелы по краям автоматически убираются.
    :return: данные из JSON, преобразованные в Python объекты (dict, list и т.д.)
    """
    with open(file_name.strip(), 'r', encoding='utf-8') as file:
        return json.load(file)


def get_type_hints_without_underscore(cls):
    """
    Возвращает словарь type hints класса, игнорируя ведущий символ '_' в имени поля.

    Например, если класс имеет аннотацию `_name: str`, в результате будет 'name': str.

    :param cls: класс, у которого извлекаются type hints
    :return: словарь {имя_поля_без_подчеркивания: тип_поля}
    """
    annotations = get_type_hints(cls)
    result = {}
    for key, value in annotations.items():
        start_index = 0
        if key[0] == '_':
            start_index = 1
        result[key[start_index:]] = value
    return result


def get_fields(source, is_common: bool = False) -> list:
    if source is None:
        raise ValueError("Некорректно переданы аргументы!")

    return list(filter(lambda x: not x.startswith("_"), dir(source)))


def load_fields_from_dict():
    ...