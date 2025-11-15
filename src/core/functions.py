import json
from typing import get_type_hints

from src.models.measurement_unit import MeasurementUnitModel


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
def measurement_unit_to_super_base(unit: MeasurementUnitModel):
    """
    Рекурсивно (через итерацию с циклом while) преобразует заданную единицу измерения
    в самую базовую (корневую) единицу в иерархии и вычисляет общий коэффициент
    преобразования от исходной единицы к этой базовой единице.

    :param unit: Исходный объект единицы измерения (MeasurementUnitModel),
                 который должен иметь поля 'conversion_factor' (множитель к базовой единице)
                 и 'base_unit' (ссылка на базовую единицу, или None для корневой).
    :return: Кортеж, содержащий:
             1. result_factor (float): Общий коэффициент, который нужно умножить
                на числовое значение в исходной единице, чтобы получить значение
                в самой базовой единице.
             2. unit (MeasurementUnitModel): Самая базовая (корневая) единица в иерархии.
    """
    result_factor = 1  # Инициализация общего коэффициента преобразования
    while True:
        # Умножаем текущий общий коэффициент на коэффициент преобразования текущей единицы
        result_factor*=unit.conversion_factor
        # Проверяем, является ли текущая единица базовой (корневой)
        if unit.base_unit is None:
            break  # Выход из цикла, если достигнута корневая единица
        # Переход к следующей базовой единице
        unit = unit.base_unit
    return result_factor, unit

def get_nested_attr(obj, field_names: list):
    """
    Получает значение вложенного атрибута из объекта, используя список имен полей.
    Например, для field_names=['address', 'city'] функция вернет obj.address.city.

    :param obj: Исходный объект, из которого нужно извлечь атрибут.
    :param field_names: Список строк, представляющих иерархию вложенных атрибутов.
    :return: Значение самого вложенного атрибута.
    :raises AttributeError: Если какой-либо атрибут не существует на соответствующем уровне.
    """
    for filed in field_names:
        # Последовательно получаем атрибут, используя getattr()
        obj = getattr(obj, filed)
    return obj