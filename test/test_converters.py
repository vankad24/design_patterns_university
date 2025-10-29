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


def test_basic_converter_primitives():
    """Проверяет конвертацию примитивных типов: int, float, str, bool, None."""
    converter = BasicConverter()

    # int
    assert converter.convert(123) == 123
    # float
    assert converter.convert(123.45) == 123.45
    # str
    assert converter.convert("test_string") == "test_string"
    # bool
    assert converter.convert(True) is True
    # None
    assert converter.convert(None) is None


def test_datetime_converter_basic():
    """Проверяет конвертацию объекта datetime в строку заданного формата."""
    converter = DatetimeConverter()
    dt = datetime(2023, 10, 26, 15, 30, 45)
    expected_format = "2023-10-26 15:30:45"

    result = converter.convert(dt)

    assert isinstance(result, str)
    assert result == expected_format

def test_dict_converter_with_primitives():
    """Проверяет конвертацию словаря с примитивными значениями (используя FactoryConverters)."""
    # FactoryConverters.convert будет использовать BasicConverter
    converter = DictConverter()
    data = {
        "key1": 1,
        "key2": "value",
        "key3": 3.14,
        "key4": True,
        "key5": None
    }

    result = converter.convert(data)

    assert isinstance(result, dict)
    assert result == data


def test_dict_converter_with_complex_types():
    """Проверяет конвертацию словаря с комплексными типами, мокая FactoryConverters.convert."""

    converter = DictConverter()

    # Значения могут быть любыми объектами, мок обрабатывает их
    gr = MeasurementUnitModel.create('gr')
    gr.id = 'fff0a80d-0b0e-4274-bdd9-148e04be36be'
    kg = MeasurementUnitModel.create('kg',1000.0, gr)
    kg.id = '7f6ec0af-a17a-474d-812a-1ea14d4f789a'
    data = {
        "key1": kg,
        "key2": datetime(2023, 1, 1),
        "key3": [1, 2],
    }

    expected = {
        'key1': {
            'id': '7f6ec0af-a17a-474d-812a-1ea14d4f789a',
            'name': 'kg',
            'conversion_factor': 1000.0,
            'base_unit': {'base_unit': None,
                          'conversion_factor': 1.0,
                          'id': 'fff0a80d-0b0e-4274-bdd9-148e04be36be',
                          'name': 'gr'},
        },
        'key2': '2023-01-01 00:00:00',
        'key3': [1, 2]
    }
    result = converter.convert(data)
    assert result == expected
    print(result)

def test_iterable_converter_with_primitives():
    """Проверяет конвертацию списка с примитивными типами (используя FactoryConverters)."""
    # FactoryConverters.convert будет использовать BasicConverter
    converter = IterableConverter()
    data = [1, "test", 3.14, True, None]

    result = converter.convert(data)

    assert isinstance(result, list)
    assert result == data


def test_iterable_converter_with_complex_types():
    """Проверяет конвертацию итерируемого объекта с комплексными типами, мокая FactoryConverters.convert."""


    converter = IterableConverter()
    data = (
        MeasurementUnitModel.create('gr'),  # Комплексный тип
        datetime(2023, 1, 1),  # Комплексный тип
        [1, 2],  # Комплексный тип
    )
    todo


def test_model_converter_simple_model():
    """Проверяет конвертацию простой модели (не содержащей вложенных моделей)."""

    model = todo
    converter = ModelConverter()

    result = converter.convert(model)

    expected = {
        todo
    }

    assert isinstance(result, dict)
    assert result == expected




def test_factory_converters_get_converter_primitives():
    """Проверяет получение BasicConverter для примитивных типов."""
    factory = FactoryConverters()

    # int, float, str, bool, None
    assert isinstance(factory.get_converter(int), BasicConverter)
    assert isinstance(factory.get_converter(float), BasicConverter)
    assert isinstance(factory.get_converter(str), BasicConverter)
    assert isinstance(factory.get_converter(bool), BasicConverter)
    assert isinstance(factory.get_converter(type(None)), BasicConverter)


def test_factory_converters_get_converter_datetime():
    """Проверяет получение DatetimeConverter для datetime."""
    factory = FactoryConverters()
    assert isinstance(factory.get_converter(datetime), DatetimeConverter)


def test_factory_converters_get_converter_model():
    """Проверяет получение ModelConverter для AbstractModel."""
    factory = FactoryConverters()
    assert isinstance(factory.get_converter(MeasurementUnitModel), ModelConverter)


def test_factory_converters_get_converter_dict():
    """Проверяет получение DictConverter для dict."""
    factory = FactoryConverters()
    assert isinstance(factory.get_converter(dict), DictConverter)


def test_factory_converters_get_converter_iterable():
    """Проверяет получение IterableConverter для list/tuple/set (Iterable)."""
    factory = FactoryConverters()
    assert isinstance(factory.get_converter(list), IterableConverter)
    assert isinstance(factory.get_converter(tuple), IterableConverter)
    assert isinstance(factory.get_converter(set), IterableConverter)


def test_factory_converters_get_converter_unsupported_type():
    """Проверяет, что для неподдерживаемого типа выбрасывается ArgumentException."""
    factory = FactoryConverters()

    class UnsupportedType:
        pass

    with pytest.raises(ArgumentException) as excinfo:
        factory.get_converter(UnsupportedType)

    assert "Не удалось создать конвертер для типа:'UnsupportedType'" in str(excinfo.value)


def test_factory_converters_convert_int():
    """Проверяет сквозную конвертацию для int (используя BasicConverter)."""
    data = 100
    result = FactoryConverters.convert(data)
    assert result == 100


def test_factory_converters_convert_datetime():
    """Проверяет сквозную конвертацию для datetime (используя DatetimeConverter)."""
    dt = datetime(2025, 1, 1, 12, 0, 0)
    result = FactoryConverters.convert(dt)
    assert result == "2025-01-01 12:00:00"


def test_factory_converters_convert_list_of_ints():
    """Проверяет сквозную конвертацию списка int (используя IterableConverter и BasicConverter)."""
    data = [1, 2, 3]
    result = FactoryConverters.convert(data)
    assert result == [1, 2, 3]  # IterableConverter использует BasicConverter для элементов


def test_factory_converters_convert_model():
    """Проверяет сквозную конвертацию модели (используя ModelConverter)."""
    model = todo

    result = FactoryConverters.convert(model)

    expected = {
        todo
    }

    assert result == expected

if __name__ == "__main__":
    pytest.main(['-v'])