from datetime import datetime

from src.core.functions import measurement_unit_to_super_base
from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
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
    def calculate(all_transactions: list[TransactionModel], all_products: dict, storage, start_date: datetime,
                  end_date: datetime):
        start = datetime(start_date.year, start_date.month, start_date.day)
        end = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        result = []

        transactions_prototype = Prototype(all_transactions)\
            .filter(FilterDto(field_name="storage", value=storage))\
            .filter(FilterDto(field_name="period", value=end, op="<"))

        data = transactions_prototype.data.copy()
        unique_product_ids = set()
        product_to_base_unit = dict()

        if data:
            *_, main_base_unit = measurement_unit_to_super_base(data[0].unit)
            for trans in data:
                factor, base_unit = measurement_unit_to_super_base(trans.unit)
                if base_unit != main_base_unit:
                    raise OperationException(f"Разные единицы измерения для {trans.product}")
                trans.value *= factor
                trans.unit = base_unit
                unique_product_ids.add(trans.product.id)
                product_to_base_unit[trans.product.id] = base_unit
            transactions_prototype = Prototype(data)

            start_transactions = transactions_prototype.filter(FilterDto(field_name="period", value=start, op="<"))
            current_transactions = transactions_prototype.filter(FilterDto(field_name="period", value=start, op=">="))
            positive_transactions = current_transactions.filter(FilterDto(field_name="value", value=0, op=">"))
            negative_transactions = current_transactions.filter(FilterDto(field_name="value", value=0, op="<"))

            for product_id in unique_product_ids:
                product = all_products[product_id]
                filter_by_product = FilterDto(field_name="product", value=product)
                start_values = start_transactions.filter(filter_by_product).data
                positive_values = positive_transactions.filter(filter_by_product).data
                negative_values = negative_transactions.filter(filter_by_product).data

                item = TurnoverBalanceItem.create(storage, product, product_to_base_unit[product_id])

                def sum_values(values):
                    return sum(map(lambda x: x.value, values))

                # Начальное сальдо
                item.start_balance = sum_values(start_values)
                # Поступления
                item.inflows = sum_values(positive_values)
                # Расходы
                item.outflows = sum_values(negative_values)

                result.append(item)

        filtered_products = Prototype(list(all_products.values())).filter(FilterDto(field_name='id', value=unique_product_ids, op="notin")).data
        for product in filtered_products:
            result.append(TurnoverBalanceItem.create(storage, product, product.unit))

        return result