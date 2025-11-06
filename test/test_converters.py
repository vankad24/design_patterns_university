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
    unit = MeasurementUnitModel.create('gr')
    unit.id = 'fff0a80d-0b0e-4274-bdd9-148e04be36be'
    return unit


@pytest.fixture
def kg(gr):
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
    converter = BasicConverter()
    factory = FactoryConverters()
    assert converter.convert(value) == value
    assert FactoryConverters.convert(value) == value
    assert isinstance(factory.get_converter(type(value)), BasicConverter)


@pytest.mark.parametrize("dt, expected", [
    (datetime(2023, 10, 26, 15, 30, 45), "2023-10-26 15:30:45"),
    (datetime(2025, 1, 1, 12, 0, 0), "2025-01-01 12:00:00"),
])
def test_datetime_converter_conversion_and_factory(dt, expected):
    converter = DatetimeConverter()
    factory = FactoryConverters()
    assert converter.convert(dt) == expected
    assert FactoryConverters.convert(dt) == expected
    assert isinstance(factory.get_converter(datetime), DatetimeConverter)


def test_dict_converter_with_complex_types(gr, kg):
    converter = DictConverter()
    data = {
        "key1": kg,
        "key2": datetime(2023, 1, 1),
        "key3": {"nested": 1},
    }

    result = converter.convert(data)

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
    converter = IterableConverter()
    assert converter.convert(data) == expected


def test_iterable_converter_with_complex_types(gr):
    converter = IterableConverter()
    data = [1, datetime(2023, 1, 1), gr]

    result = converter.convert(data)

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
    model = MeasurementUnitModel.create(unit_name)
    model.id = 'aff0a80d-0b0e-4321-bdd9-148e04be36bf'

    result = ModelConverter().convert(model)

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
    factory = FactoryConverters()
    assert isinstance(factory.get_converter(type_input), expected_converter)


def test_factory_converters_get_converter_unsupported_type():
    class UnsupportedType:
        pass

    with pytest.raises(ArgumentException) as exc:
        FactoryConverters.get_converter(UnsupportedType)

    assert "Не удалось создать конвертер для типа:'UnsupportedType'" in str(exc.value)


def test_factory_converters_convert_list_of_ints():
    """Проверяет сквозную конвертацию списка int (используя IterableConverter и BasicConverter)."""
    data = [1, 2, 3]
    result = FactoryConverters.convert(data)
    assert result == [1, 2, 3]


if __name__ == "__main__":
    pytest.main(['-v'])