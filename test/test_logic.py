from datetime import datetime

import pytest

from src.dto.filter_dto import FilterDto
from src.dto.filter_tbs_dto import FilterTbsDto
from src.logics.factory_entities import FactoryEntities
from src.logics.responses.abstract_response import AbstractResponse
from src.logics.responses.csv_response import CsvResponse
from src.logics.responses.response_format import ResponseFormat
from src.logics.turnover_balance_sheet import TurnoverBalanceSheet
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.product_remain import ProductRemainModel
from src.models.storage import StorageModel
from src.models.transaction import TransactionModel


@pytest.fixture
def base_unit():
    """Единица измерения: шт."""
    return MeasurementUnitModel.create(name='pc')

@pytest.fixture
def storage_a():
    """Склад A, основной склад для тестирования."""
    return StorageModel.create(name='Склад А', address='Улица А')

@pytest.fixture
def storage_b():
    """Склад B, для проверки фильтрации по складу."""
    return StorageModel.create(name='Склад Б', address='Улица Б')

@pytest.fixture
def product_a(base_unit):
    """Продукт А, по которому есть движения."""
    return ProductModel.create(name='Продукт А', unit=base_unit)

@pytest.fixture
def product_b(base_unit):
    """Продукт Б, по которому нет движений в рамках периода/склада."""
    return ProductModel.create(name='Продукт Б', unit=base_unit)

@pytest.fixture
def all_products(product_a, product_b):
    """Словарь всех продуктов, используемый в расчете."""
    return {
        product_a.id: product_a,
        product_b.id: product_b
    }

def test_create_response_csv_not_none():
    """
    Проверяет, что CsvResponse корректно строит ответ (не None)
    при передаче ему валидных данных.
    """
    # Подготовка
    response = CsvResponse()
    data = [ProductGroupModel.create("test")]

    # Действие
    result = response.build(data)

    # Проверки
    assert result is not None


def test_factory_create_not_none_create():
    """
    Проверяет работу FactoryEntities:
    1. Что фабрика успешно создает класс-ответ (logic).
    2. Что созданный класс наследует AbstractResponse.
    3. Что экземпляр этого класса может построить непустую строку ответа.
    """
    # Подготовка
    factory = FactoryEntities()
    data = [ProductGroupModel.create("test")]

    # Действие
    logic = factory.create(ResponseFormat.CSV)

    # Проверки
    assert logic is not None

    # Действие
    instance = logic()
    # Проверки
    assert isinstance(instance, AbstractResponse)

    # Действие
    text = instance.build(data)
    # Проверки
    assert len(text) > 0

def test_tbs_calculation_full_scenario(storage_a, storage_b, product_a, product_b, base_unit, all_products):
    """
    Проверяет комплексный сценарий с использованием реальных моделей:
    Начальное сальдо, Приход/Расход, Фильтрация по складу и дате, Продукт без движений.
    """
    # Подготовка
    START_DATE = datetime(2024, 1, 1)
    END_DATE = datetime(2024, 1, 31)

    all_transactions = [
        # 1. Начальное сальдо для Prod A (период ДО)
        TransactionModel.create(datetime(2023, 12, 15), 50.0, base_unit, product_a, storage_a),
        TransactionModel.create(datetime(2023, 12, 20), -10.0, base_unit, product_a, storage_a), # Начальное сальдо: 50 - 10 = 40.0

        # 2. Движения в периоде (ВХОД)
        TransactionModel.create(datetime(2024, 1, 10), 100.0, base_unit, product_a, storage_a),

        # 3. Движения в периоде (РАСХОД)
        TransactionModel.create(datetime(2024, 1, 20), -25.0, base_unit, product_a, storage_a),

        # 4. Транзакция на другом складе (должна быть ИГНОРИРОВАНА)
        TransactionModel.create(datetime(2024, 1, 15), 5.0, base_unit, product_a, storage_b),

        # 5. Транзакция ПОСЛЕ периода (должна быть ИГНОРИРОВАНА)
        TransactionModel.create(datetime(2024, 2, 1), 999.0, base_unit, product_a, storage_a),
    ]
    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage_a)])

    # Действие
    result_list = TurnoverBalanceSheet.calculate(all_transactions, all_products, dto, START_DATE, END_DATE)

    # Проверки
    assert len(result_list) == 2

    item_a = next((item for item in result_list if item.product.id == product_a.id), None)
    item_b = next((item for item in result_list if item.product.id == product_b.id), None)
    assert item_a is not None
    assert item_b is not None

    # Prod A
    assert item_a.start_balance == 40.0
    assert item_a.inflows == 100.0
    assert item_a.outflows == -25.0
    assert item_a.end_balance == 115.0

    # Prod B (без движений)
    assert item_b.start_balance == 0.0


def test_tbs_calculation_empty_transactions(storage_a, all_products):
    """Проверяет, что расчет для пустого списка транзакций возвращает 0 для всех продуктов."""
    # Подготовка
    START_DATE = datetime(2024, 1, 1)
    END_DATE = datetime(2024, 1, 31)
    all_transactions = []
    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage_a)])

    # Действие
    result_list = TurnoverBalanceSheet.calculate(all_transactions, all_products, dto, START_DATE, END_DATE)

    # Проверки
    assert len(result_list) == 2
    for item in result_list:
        assert item.end_balance == 0.0


def test_tbs_calculation_with_product_remains(storage_a, product_a, product_b, base_unit, all_products):
    """
    Проверяет, что начальное сальдо корректно берется из `product_remains`,
    а не из транзакций до `start_date`.
    """
    START_DATE = datetime(2024, 1, 10)
    END_DATE = datetime(2024, 1, 31)

    all_transactions = [
        TransactionModel.create(datetime(2024, 1, 5), 50.0, base_unit, product_a, storage_a),
        # Движения в периоде
        TransactionModel.create(datetime(2024, 1, 15), 10.0, base_unit, product_a, storage_a),  # Приход
        TransactionModel.create(datetime(2024, 1, 20), -5.0, base_unit, product_a, storage_a),  # Расход
    ]

    # Начальный остаток (Product A на Storage A)
    initial_remain_a = ProductRemainModel.create(
        value=100.0,  # Начальное сальдо
        unit_model=base_unit,
        product_model=product_a,
        storage_model=storage_a
    )

    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage_a)])

    # Действие
    result_list = TurnoverBalanceSheet.calculate(
        all_transactions,
        all_products,
        dto,
        START_DATE,
        END_DATE,
        product_remains=[initial_remain_a]
    )

    # Проверки
    item_a = next((item for item in result_list if item.product.id == product_a.id), None)
    assert item_a is not None

    # Начальное сальдо берется из initial_remain_a (100.0) + 50.0
    assert item_a.start_balance == 150.0
    # Приход: 10.0
    assert item_a.inflows == 10.0
    # Расход: -5.0
    assert item_a.outflows == -5.0
    # Конечное сальдо: 150.0 + 10.0 - 5.0 = 155.0
    assert item_a.end_balance == 155.0

    # Проверка, что продукт без остатков/движений тоже есть в списке (по умолчанию)
    item_b = next((item for item in result_list if item.product.id == product_b.id), None)
    assert item_b is not None
    assert item_b.start_balance == 0.0



def test_tbs_calculation_with_block_date_and_transactions(storage_a, product_a, storage_b, base_unit, all_products):
    """
    Проверяет расчет сальдо, когда задана `block_date`.
    """
    START_DATE = datetime(2024, 1, 16)
    END_DATE = datetime(2024, 1, 31)
    BLOCK_DATE = datetime(2024, 1, 4)  # Блокировка/закрытие ведомости до этой даты

    all_transactions = [
        # Транзакции в закрытом периоде до BLOCK_DATE (добавляются в начальное сальдо)
        TransactionModel.create(datetime(2024, 1, 5), 50.0, base_unit, product_a, storage_a),
        TransactionModel.create(datetime(2024, 1, 13), 40.0, base_unit, product_a, storage_b),
        TransactionModel.create(datetime(2024, 1, 14), -20.0, base_unit, product_a, storage_a),

        # Транзакции в ОТКРЫТОМ периоде (BLOCK_DATE <= date <= END_DATE)
        TransactionModel.create(datetime(2024, 1, 16), 10.0, base_unit, product_a, storage_a),  # Приход
        TransactionModel.create(datetime(2024, 1, 17), 10.0, base_unit, product_a, storage_b),  # Приход
        TransactionModel.create(datetime(2024, 1, 25), -5.0, base_unit, product_a, storage_a),  # Расход
    ]

    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage_a)])

    # Начальный остаток (Product A на Storage A)
    initial_remain_a = ProductRemainModel.create(
        value=20.0,
        unit_model=base_unit,
        product_model=product_a,
        storage_model=storage_a
    )

    # Действие
    result_list = TurnoverBalanceSheet.calculate(
        all_transactions,
        all_products,
        dto,
        START_DATE,
        END_DATE,
        block_date=BLOCK_DATE,
        product_remains=[initial_remain_a]
    )

    # Проверки
    item_a = next((item for item in result_list if item.product.id == product_a.id), None)
    assert item_a is not None

    # Начальное сальдо: Начальный остаток (20.0) Транзакции до BLOCK_DATE (50.0 - 20.0 = 30.0)
    assert item_a.start_balance == 50.0
    # Приход: 10.0
    assert item_a.inflows == 10.0
    # Расход: -5.0
    assert item_a.outflows == -5.0
    # Конечное сальдо: 50.0 + 10.0 - 5.0 = 55.0
    assert item_a.end_balance == 55.0



def test_tbs_calculation_no_zero_values(storage_a, product_a, product_b, base_unit, all_products):
    """
    Проверяет фильтрацию `include_zero_values=False`, когда продукт не должен попасть в результат.
    """
    START_DATE = datetime(2024, 1, 1)
    END_DATE = datetime(2024, 1, 31)

    all_transactions = [
        # Движения только для Prod A
        TransactionModel.create(datetime(2024, 1, 10), 50.0, base_unit, product_a, storage_a),
    ]

    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage_a)])

    # Действие: include_zero_values=False
    result_list = TurnoverBalanceSheet.calculate(
        all_transactions,
        all_products,
        dto,
        START_DATE,
        END_DATE,
        include_zero_values=False
    )

    # Проверки
    # Ожидаем только 1 продукт (Prod A)
    assert len(result_list) == 1
    item_a = next((item for item in result_list if item.product.id == product_a.id), None)
    item_b = next((item for item in result_list if item.product.id == product_b.id), None)

    assert item_a is not None
    assert item_b is None  # Prod B отсутствует, так как все его значения 0.0


def test_tbs_calculation_date_boundary(storage_a, product_a, base_unit, all_products):
    """
    Проверяет, что транзакции, ровно совпадающие с `start` и `end` датами,
    корректно обрабатываются.
    """
    START_DATE = datetime(2024, 1, 1)
    END_DATE = datetime(2024, 1, 31)

    all_transactions = [
        # Транзакция на start_date ДОЛЖНА быть учтена как Приход/Расход, не как начальное сальдо
        TransactionModel.create(START_DATE, 10.0, base_unit, product_a, storage_a),
        # Транзакция на end_date ДОЛЖНА быть учтена
        TransactionModel.create(END_DATE, -5.0, base_unit, product_a, storage_a),
        # Транзакция ДО start_date (Начальное сальдо)
        TransactionModel.create(datetime(2023, 12, 31), 5.0, base_unit, product_a, storage_a),
    ]

    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage_a)])

    # Действие
    result_list = TurnoverBalanceSheet.calculate(all_transactions, all_products, dto, START_DATE, END_DATE)

    # Проверки
    item_a = next((item for item in result_list if item.product.id == product_a.id), None)
    assert item_a is not None

    # Начальное сальдо: 5.0 (транзакция до START_DATE)
    assert item_a.start_balance == 5.0
    # Приход: 10.0 (транзакция на START_DATE)
    assert item_a.inflows == 10.0
    # Расход: -5.0 (транзакция на END_DATE)
    assert item_a.outflows == -5.0
    # Конечное сальдо: 5.0 + 10.0 - 5.0 = 10.0
    assert item_a.end_balance == 10.0


if __name__ == "__main__":
    pytest.main(['-v'])