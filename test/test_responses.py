import pytest

from src.logics.responses.csv_response import CsvResponse
from src.logics.responses.error_response import ErrorResponse
from src.logics.responses.json_response import JsonResponse
from src.logics.responses.markdown_response import MarkdownResponse
from src.repository import RepoKeys
from src.start_service import StartService


@pytest.fixture
def service():
    return StartService('../settings.json')

@pytest.fixture
def products(service):
    return list(service.repo.data[RepoKeys.PRODUCTS].values())

# Проверить формирование Markdown
def test_markdown_response_build(products):
    # Подготовка
    response = MarkdownResponse()

    # Действие
    result = response.build(products)

    # Проверка
    assert len(result) > 0
    print(result)


# Проверить формирование Json
def test_json_response_build(products):
    # Подготовка
    response = JsonResponse()

    # Действие
    result = response.build(products)

    # Проверка
    assert len(result) > 0
    print(result)

# Проверить формирование csv
def test_csv_response_build(products):
    # Подготовка
    response = CsvResponse()

    # Действие
    result = response.build(products)

    # Проверка
    assert len(result) > 0
    print(result)

# Проверить формирование error response
def test_error_response_build(products):
    # Подготовка
    response = ErrorResponse()

    # Действие
    result = response.build("some error")

    # Проверка
    assert result == "Error response: some error"

