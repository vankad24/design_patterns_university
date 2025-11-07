from datetime import datetime

import pytest

from src.logics.converters.basic_converter import BasicConverter
from src.logics.converters.datetime_converter import DatetimeConverter
from src.logics.converters.dict_converter import DictConverter
from src.logics.converters.iterable_converter import IterableConverter
from src.logics.converters.model_converter import ModelConverter
from src.logics.factory_converters import FactoryConverters
from src.models.measurement_unit import MeasurementUnitModel
from src.models.validators.exceptions import ArgumentException


@pytest.fixture
def gr():
    """
    pytest-фикстура, создающая базовую единицу измерения 'gr' (грамм).
    Присваивает ей фиксированный ID для предсказуемых результатов в тестах.
    """
    unit = MeasurementUnitModel.create('gr')
    unit.id = 'fff0a80d-0b0e-4274-bdd9-148e04be36be'
    return unit


@pytest.fixture
def kg(gr):
    """
    pytest-фикстура, создающая производную единицу измерения 'kg' (килограмм).
    Определяет ее как 1000.0 базовых единиц 'gr'.
    Присваивает ей фиксированный ID.
    """
    unit = MeasurementUnitModel.create('kg', 1000.0, gr)
    unit.id = '7f6ec0af-a17a-474d-812a-1ea14d4f789a'
    return unit


@pytest.mark.parametrize("value", [
    123,
    123.45,
    "test_string",
    True,
    None,
])
def test_basic_converter_and_factory_for_primitives(value):
    """
    Тест проверяет, что BasicConverter и FactoryConverters корректно обрабатывают
    базовые (примитивные) типы данных, возвращая их без изменений,
    и что Factory выбирает правильный конвертер.
    """
    # Подготовка
    converter = BasicConverter()
    factory = FactoryConverters()
    # Действие и Проверка (внутри утверждений)
    assert converter.convert(value) == value
    assert FactoryConverters.convert(value) == value
    assert isinstance(factory.get_converter(type(value)), BasicConverter)


@pytest.mark.parametrize("dt, expected", [
    (datetime(2023, 10, 26, 15, 30, 45), "2023-10-26 15:30:45"),
    (datetime(2025, 1, 1, 12, 0, 0), "2025-01-01 12:00:00"),
])
def test_datetime_converter_conversion_and_factory(dt, expected):
    """
    Тест проверяет, что DatetimeConverter правильно форматирует объекты datetime
    в строку и что FactoryConverters корректно выбирает этот конвертер.
    """
    # Подготовка
    converter = DatetimeConverter()
    factory = FactoryConverters()
    # Действие и Проверка (внутри утверждений)
    assert converter.convert(dt) == expected
    assert FactoryConverters.convert(dt) == expected
    assert isinstance(factory.get_converter(datetime), DatetimeConverter)


def test_dict_converter_with_complex_types(gr, kg):
    """
    Тест проверяет работу DictConverter с вложенными комплексными типами
    (другими моделями, datetime) и его способность рекурсивно их конвертировать.
    """
    # Подготовка
    converter = DictConverter()
    data = {
        "key1": kg,
        "key2": datetime(2023, 1, 1),
        "key3": {"nested": 1},
    }
    # Действие
    result = converter.convert(data)
    # Проверка
    assert result == {
        'key1': {
            'id': kg.id,
            'name': 'kg',
            'conversion_factor': 1000.0,
            'base_unit': {
                'id': gr.id,
                'name': 'gr',
                'conversion_factor': 1.0,
                'base_unit': None
            }
        },
        'key2': "2023-01-01 00:00:00",
        'key3': {"nested": 1}
    }


@pytest.mark.parametrize("data, expected", [
    ([1, "test", 3.14, True, None], [1, "test", 3.14, True, None]),
    ([1, [2, 3]], [1, [2, 3]]),
])
def test_iterable_converter_with_primitives(data, expected):
    """
    Тест проверяет, что IterableConverter правильно обрабатывает итерируемые
    объекты (списки/кортежи) с примитивными типами данных.
    """
    # Подготовка
    converter = IterableConverter()
    # Действие и Проверка
    assert converter.convert(data) == expected


def test_iterable_converter_with_complex_types(gr):
    """
    Тест проверяет, что IterableConverter правильно обрабатывает итерируемые
    объекты, содержащие комплексные типы (datetime, пользовательские модели),
    рекурсивно применяя к ним конвертеры.
    """
    # Подготовка
    converter = IterableConverter()
    data = [1, datetime(2023, 1, 1), gr]
    # Действие
    result = converter.convert(data)
    # Проверка
    assert result == [
        1,
        "2023-01-01 00:00:00",
        {
            "id": gr.id,
            "name": "gr",
            "conversion_factor": 1.0,
            "base_unit": None
        }
    ]


@pytest.mark.parametrize("unit_name", ["liter", "gram", "piece"])
def test_model_converter_simple_model(unit_name):
    """
    Тест проверяет, что ModelConverter правильно преобразует простую
    пользовательскую модель (MeasurementUnitModel) в словарь.
    """
    # Подготовка
    model = MeasurementUnitModel.create(unit_name)
    model.id = 'aff0a80d-0b0e-4321-bdd9-148e04be36bf'
    # Действие
    result = ModelConverter().convert(model)
    # Проверка
    assert result == {
        "id": 'aff0a80d-0b0e-4321-bdd9-148e04be36bf',
        "name": unit_name,
        "conversion_factor": 1.0,
        "base_unit": None
    }

@pytest.mark.parametrize("type_input, expected_converter", [
    (int, BasicConverter),
    (float, BasicConverter),
    (str, BasicConverter),
    (bool, BasicConverter),
    (type(None), BasicConverter),
    (datetime, DatetimeConverter),
    (MeasurementUnitModel, ModelConverter),
    (dict, DictConverter),
    (list, IterableConverter),
    (tuple, IterableConverter),
    (set, IterableConverter),
])
def test_factory_converters_get_converter(type_input, expected_converter):
    """
    Тест проверяет, что FactoryConverters.get_converter корректно определяет
    и возвращает нужный класс конвертера для широкого спектра типов.
    """
    # Подготовка
    factory = FactoryConverters()
    # Действие и Проверка
    assert isinstance(factory.get_converter(type_input), expected_converter)


def test_factory_converters_get_converter_unsupported_type():
    """
    Тест проверяет, что FactoryConverters.get_converter выбрасывает
    ArgumentException при попытке получить конвертер для неподдерживаемого типа.
    """
    # Подготовка (вложенный класс-заглушка)
    class UnsupportedType:
        pass
    # Действие и Проверка
    with pytest.raises(ArgumentException) as exc:
        FactoryConverters.get_converter(UnsupportedType)

    assert "Не удалось создать конвертер для типа:'UnsupportedType'" in str(exc.value)


def test_factory_converters_convert_list_of_ints():
    """Проверяет сквозную конвертацию списка int (используя IterableConverter и BasicConverter)."""
    # Подготовка
    data = [1, 2, 3]
    # Действие
    result = FactoryConverters.convert(data)
    # Проверка
    assert result == [1, 2, 3]

if __name__ == "__main__":
    pytest.main(['-v'])