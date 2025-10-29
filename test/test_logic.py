import pytest

from src.logics.factory_entities import FactoryEntities
from src.logics.responses.abstract_response import AbstractResponse
from src.logics.responses.csv_response import CsvResponse
from src.logics.responses.response_format import ResponseFormat

from src.models.product_group import ProductGroupModel


def test_create_response_csv_not_none():
    # Подготовка
    response = CsvResponse()
    data = [ProductGroupModel.create("test")]

    # Действие
    result = response.build(data)

    # Проверки
    assert result is not None

def test_factory_create_not_none_create():
    factory = FactoryEntities()
    data = [ProductGroupModel.create("test")]

    logic = factory.create(ResponseFormat.CSV)

    assert logic is not None

    instance = logic()
    assert isinstance(instance, AbstractResponse)
    text = instance.build(data)
    assert len(text)>0




if __name__ == "__main__":
    pytest.main(['-v'])