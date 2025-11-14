import pytest

from src.core.functions import get_nested_attr
from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
from src.repository import RepoKeys
from src.start_service import StartService


@pytest.fixture
def service():
    return StartService('../settings.json')

# Тестовый класс для проверки
class Dummy:
    def __init__(self, value=None):
        self.value = value

def test_prototype_filter(service):
    # Подготовка
    repo = service.repo
    all_transactions = list(repo.data[RepoKeys.TRANSACTIONS].values())
    all_products = list(repo.data[RepoKeys.PRODUCTS].values())
    first_product = all_products[0]
    start_prototype = Prototype(all_transactions)

    # Действие
    next_prototype = start_prototype.filter(FilterDto(field_name="product", value=first_product))

    # Проверки
    assert len(all_transactions) > 0
    assert len(all_products) > 0
    assert len(next_prototype.data) > 0
    assert len(start_prototype.data) > 0
    assert len(start_prototype.data) >= len(next_prototype.data)
    assert next_prototype.data[0].product == first_product

def test_get_nested_attr_success():
    # Подготовка
    inner = Dummy(value=42)
    middle = Dummy(value=inner)
    outer = Dummy(value=middle)

    # Действие
    result = get_nested_attr(outer, ['value', 'value', 'value'])
    result2 = get_nested_attr(inner, ['value'])

    # Проверки
    assert result == 42
    assert result2 == 42

if __name__ == "__main__":
    pytest.main(['-v'])