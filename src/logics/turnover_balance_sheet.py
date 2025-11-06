from dataclasses import dataclass
from datetime import datetime

from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.storage import StorageModel
from src.models.transaction import TransactionModel
from src.models.validators.exceptions import OperationException


# Класс для хранения значений сальдовой ведомости конкретного продукта
@dataclass
class TurnoverBalanceItem:
    storage: StorageModel
    product: ProductModel
    unit: MeasurementUnitModel
    start_balance: float = 0.0 # Начальное сальдо (остаток)
    inflows: float = 0.0 # Поступления
    outflows: float = 0.0 # Расходы
    @property
    def change_in_balance(self): # Изменение за период
        return self.inflows+self.outflows
    @property
    def end_balance(self): # Конечное сальдо
        return self.start_balance+self.change_in_balance


# Класс для подсчёта сальдовой ведомости
class TurnoverBalanceSheet:
    # Функция подсчёта сальдовой ведомости по продуктам для конкретного склада
    @staticmethod
    def calculate(all_transactions: list[TransactionModel], all_products: dict, storage, start_date: datetime, end_date: datetime):
        start = datetime(start_date.year, start_date.month, start_date.day)
        end = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        turnover_balances: dict[str, TurnoverBalanceItem] = {}

        for trans in all_transactions:
            if trans.storage == storage and trans.period < end:
                pr_id = trans.product.id
                if pr_id not in turnover_balances:
                    turnover_balances[pr_id] = TurnoverBalanceItem(trans.storage, trans.product, trans.unit)
                item = turnover_balances[pr_id]
                if item.unit!=trans.unit:
                    # todo добавить поддержку перевода в разные единицы измерения
                    raise OperationException(f"Разные единицы измерения для {item.product}")

                if trans.period < start:
                    # Начальное сальдо
                    item.start_balance += trans.value
                else:
                    if trans.value > 0:
                        # Поступления
                        item.inflows += trans.value
                    else:
                        # Расходы
                        item.outflows += trans.value

        result = list(turnover_balances.values())
        other_product_ids = set(all_products.keys()) - set(turnover_balances.keys())
        for key in other_product_ids:
            product = all_products[key]
            result.append(TurnoverBalanceItem(storage, product, product.unit))

        return result