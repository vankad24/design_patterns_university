import pytest

from src.logics.responses.markdown_response import MarkdownResponse
from src.repository import RepoKeys
from src.start_service import StartService


@pytest.fixture
def service():
    return StartService('../settings.json')

# Проверить формирование Markdown
def test_markdown_response_build(service):
    # Подготовка
    response = MarkdownResponse()

    # Действие
    result = response.build(list(service.repo.data[RepoKeys.PRODUCTS].values()))

    # Проверка
    assert len(result) > 0
    print(result)

