import pytest

from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
from src.repository import RepoKeys
from src.start_service import StartService


@pytest.fixture
def service():
    return StartService('../settings.json')

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



if __name__ == "__main__":
    pytest.main(['-v'])