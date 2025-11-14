from datetime import datetime

from src.core.functions import measurement_unit_to_super_base
from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
from src.dto.filter_tbs_dto import FilterTbsDto
from src.models.tbs_item import TurnoverBalanceItem
from src.models.transaction import TransactionModel
from src.models.validators.exceptions import OperationException


# Класс для подсчёта сальдовой ведомости
class TurnoverBalanceSheet:
    # Функция подсчёта сальдовой ведомости по продуктам для конкретного склада
    # осталась на память
    @staticmethod
    def calculate_old(all_transactions: list[TransactionModel], all_products: dict, storage, start_date: datetime, end_date: datetime):
        start = datetime(start_date.year, start_date.month, start_date.day)
        end = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        turnover_balances: dict[str, TurnoverBalanceItem] = {}

        for trans in all_transactions:
            if trans.storage == storage and trans.period < end:
                pr_id = trans.product.id
                if pr_id not in turnover_balances:
                    turnover_balances[pr_id] = TurnoverBalanceItem.create(trans.storage, trans.product, trans.unit)
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
            result.append(TurnoverBalanceItem.create(storage, product, product.unit))

        return result


    # Функция подсчёта сальдовой ведомости по продуктам для конкретного склада
    @staticmethod
    def calculate(all_transactions: list[TransactionModel], all_products: dict, dto: FilterTbsDto):
        start = datetime.strptime(dto.start_date, '%Y-%m-%d')
        end = datetime.strptime(dto.end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        result = []

        transactions_prototype = Prototype(all_transactions)\
            .filter(FilterDto(field_name="period", value=end, op="<"))\
            .filter_mul(dto.transaction_filters)

        data = transactions_prototype.data.copy()
        unique_product_ids = set()
        id_to_storage = dict()
        product_to_base_unit = dict()

        if data:
            for trans in data:
                factor, base_unit = measurement_unit_to_super_base(trans.unit)
                trans.value *= factor
                trans.unit = base_unit

                id_to_storage[trans.storage.id] = trans.storage

                pid = trans.product.id
                unique_product_ids.add(pid)
                if pid not in product_to_base_unit:
                    product_to_base_unit[pid] = base_unit
                if base_unit != product_to_base_unit[pid]:
                    raise OperationException(f"Разные единицы измерения {base_unit} и {product_to_base_unit[pid]} для {trans.product}")
            transactions_prototype = Prototype(data)

            start_transactions = transactions_prototype.filter(FilterDto(field_name="period", value=start, op="<"))
            current_transactions = transactions_prototype.filter(FilterDto(field_name="period", value=start, op=">="))
            positive_transactions = current_transactions.filter(FilterDto(field_name="value", value=0, op=">"))
            negative_transactions = current_transactions.filter(FilterDto(field_name="value", value=0, op="<"))

            for storage_id in id_to_storage:
                storage = id_to_storage[storage_id]
                filter_by_storage = FilterDto(field_name="storage", value=storage)
                for product_id in unique_product_ids:
                    product = all_products[product_id]
                    filter_by_product = FilterDto(field_name="product", value=product)
                    start_values = start_transactions.filter_mul([filter_by_storage, filter_by_product]).data
                    positive_values = positive_transactions.filter_mul([filter_by_storage, filter_by_product]).data
                    negative_values = negative_transactions.filter_mul([filter_by_storage, filter_by_product]).data

                    item = TurnoverBalanceItem.create(storage, product, product_to_base_unit[product_id])

                    def sum_values(values):
                        return float(sum(map(lambda x: x.value, values)))

                    # Начальное сальдо
                    item.start_balance = sum_values(start_values)
                    # Поступления
                    item.inflows = sum_values(positive_values)
                    # Расходы
                    item.outflows = sum_values(negative_values)

                    result.append(item)

        filtered_products = Prototype(list(all_products.values())).filter(FilterDto(field_name='id', value=unique_product_ids, op="notin")).data
        for product in filtered_products:
            result.append(TurnoverBalanceItem.create(None, product, product.unit))

        return Prototype(result).filter_mul(dto.result_filters).sort(dto.result_sorts).data