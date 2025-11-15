import pytest

from src.core.functions import get_nested_attr
from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto
from src.repository import RepoKeys
from src.start_service import StartService


@pytest.fixture
def service():
    """
    Фикстура pytest для инициализации и предоставления экземпляра StartService.
    Она загружает настройки из указанного файла ('../settings.json').

    :return: Экземпляр StartService, готовый к использованию в тестах.
    """
    return StartService('../settings.json')

# Тестовый класс для проверки
class Dummy:
    """
    Простой вспомогательный класс, используемый в тестах для имитации
    объекта с одним атрибутом 'value'. Применяется для проверки доступа
    к вложенным атрибутам.
    """
    def __init__(self, value=None):
        """
        Конструктор класса Dummy.
        :param value: Значение, присваиваемое атрибуту 'value'.
        """
        self.value = value

def test_prototype_filter(service):
    """
    Тест проверяет корректность метода 'filter' класса Prototype.
    Он фильтрует список транзакций по заданному продукту.

    :param service: Фикстура StartService, предоставляющая доступ к репозиторию.
    """
    # Подготовка
    repo = service.repo  # Получение репозитория из сервиса
    # Получение всех транзакций и продуктов из репозитория
    all_transactions = list(repo.data[RepoKeys.TRANSACTIONS].values())
    all_products = list(repo.data[RepoKeys.PRODUCTS].values())
    first_product = all_products[0]  # Выбор первого продукта для фильтрации
    start_prototype = Prototype(all_transactions)  # Создание Прототипа с исходными данными

    # Действие
    # Применение фильтра: выбрать все транзакции, где поле 'product' равно first_product
    next_prototype = start_prototype.filter(FilterDto(field_name="product", value=first_product))

    # Проверки
    assert len(all_transactions) > 0  # Исходный набор транзакций не пуст
    assert len(all_products) > 0  # Исходный набор продуктов не пуст
    assert len(next_prototype.data) > 0  # Отфильтрованный результат не пуст
    assert len(start_prototype.data) > 0  # Исходный Прототип не пуст
    # Размер отфильтрованных данных должен быть меньше или равен размеру исходных данных
    assert len(start_prototype.data) >= len(next_prototype.data)
    # Первый элемент отфильтрованных данных должен соответствовать условию фильтрации
    assert next_prototype.data[0].product == first_product

def test_get_nested_attr_success():
    """
    Тест проверяет корректность функции 'get_nested_attr' для доступа
    к вложенным атрибутам в структуре.
    """
    # Подготовка
    # Создание иерархии вложенных объектов Dummy: outer -> middle -> inner -> 42
    inner = Dummy(value=42)
    middle = Dummy(value=inner)
    outer = Dummy(value=middle)

    # Действие
    # Получение значения 'outer.value.value.value'
    result = get_nested_attr(outer, ['value', 'value', 'value'])
    # Получение значения 'inner.value'
    result2 = get_nested_attr(inner, ['value'])

    # Проверки
    assert result == 42  # Проверка глубокого вложенного доступа
    assert result2 == 42  # Проверка простого доступа


def test_prototype_sort_multi_field_nested(service):
    """
    Тест проверяет корректность метода 'sort' класса Prototype.
    Проверяет сортировку по нескольким полям, включая одно вложенное,
    и в обратном порядке (descending=True).
    """
    # Подготовка
    all_transactions = service.repo.get_values(RepoKeys.TRANSACTIONS)
    start_prototype = Prototype(all_transactions)

    # DTO для сортировки: сначала по дате, затем по id продукта
    sort_dto = SortingDto(
        field_names=["period", "product.id"],
        descending=True  # Сортировка по обоим полям в обратном порядке (DESC)
    )

    # Действие
    sorted_prototype = start_prototype.sort(sort_dto)

    # Проверки
    assert sorted_prototype is not start_prototype  # Должен быть создан новый экземпляр (клон)
    assert len(sorted_prototype.data) == len(all_transactions)  # Длина списка не должна измениться

    # Проверка порядка сортировки
    sorted_data = sorted_prototype.data

    # Проверяем, что элементы расположены в порядке убывания
    is_sorted_descending = True
    for i in range(len(sorted_data) - 1):
        item1 = sorted_data[i]
        item2 = sorted_data[i + 1]

        # Получаем значения для первого поля ("period")
        date1 = get_nested_attr(item1, ["period"])
        date2 = get_nested_attr(item2, ["period"])

        # Если date1 < date2, то сортировка не в обратном порядке
        if date1 < date2:
            is_sorted_descending = False
            break

        # Если даты равны, проверяем второе поле ('product.id')
        if date1 == date2:
            product_id1 = get_nested_attr(item1, ['product', 'id'])
            product_id2 = get_nested_attr(item2, ['product', 'id'])

            # Если product_id1 < product_id2, то сортировка не в обратном порядке
            if product_id1 < product_id2:
                is_sorted_descending = False
                break

    assert is_sorted_descending, "Список отсортирован неправильно или не по убыванию."

if __name__ == "__main__":
    pytest.main(['-v'])