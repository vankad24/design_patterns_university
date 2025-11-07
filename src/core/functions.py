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

def dump_json(data, file_name):
    """
    Сохраняет JSON-данные в файл.

    :param data: загружаемые данные
    :param file_name: путь к файлу JSON (строка). Пробелы по краям автоматически убираются.
    """
    with open(file_name.strip(), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


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


def get_fields(obj, include_private=False, include_callable=False):
    """
        Извлекает все атрибуты (поля и методы) из заданного объекта и возвращает их в виде словаря.

        Позволяет фильтровать служебные (начинающиеся с '_') и вызываемые (методы) атрибуты
        с помощью флагов 'include_private' и 'include_callable'.

        :param obj: Объект, из которого нужно извлечь атрибуты.
        :param include_private: Если True, включать атрибуты, начинающиеся с нижнего подчеркивания (например, _name).
        :param include_callable: Если True, включать вызываемые атрибуты (методы).
        :return: Словарь, где ключ — имя атрибута, а значение — его содержимое.
        :raises ValueError: Если переданный объект None.
    """
    if obj is None:
        raise ValueError("Некорректно переданы аргументы!")

    result = dict()
    for key in dir(obj):
        value = getattr(obj, key)
        if (not key.startswith("_") or include_private) and (not callable(value) or include_callable):
            result[key] = value
    return result
