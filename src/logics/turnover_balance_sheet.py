from datetime import datetime

from src.core.functions import measurement_unit_to_super_base
from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
from src.dto.filter_tbs_dto import FilterTbsDto
from src.models.product_remain import ProductRemainModel
from src.models.tbs_item import TurnoverBalanceItem
from src.models.transaction import TransactionModel
from src.models.validators.exceptions import OperationException
from src.repository import Repository, RepoKeys
from src.settings_manager import SettingsManager


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


    # Функция подсчёта сальдовой ведомости по продуктам с фильтрацией и сортировкой используя данные из dto
    @staticmethod
    def calculate(all_transactions: list[TransactionModel], all_products: dict, dto: FilterTbsDto, start: datetime, end: datetime, block_date: datetime = None, product_remains: list[ProductRemainModel]=[], include_zero_values=True):
        result = []

        transactions_prototype = Prototype(all_transactions)\
            .filter(FilterDto(field_name="period", value=end, op="<"))\
            .filter_mul(dto.transaction_filters)

        if block_date:
            transactions_prototype = transactions_prototype.filter(FilterDto(field_name="period", value=block_date, op=">="))

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

            start_balance_proto = transactions_prototype.filter(FilterDto(field_name="period", value=start, op="<"))
            current_period_proto = transactions_prototype.filter(FilterDto(field_name="period", value=start, op=">="))
            positive_values_proto = current_period_proto.filter(FilterDto(field_name="value", value=0, op=">"))
            negative_values_proto = current_period_proto.filter(FilterDto(field_name="value", value=0, op="<"))
            product_remains_proto = Prototype(product_remains)

            for storage_id in id_to_storage:
                storage = id_to_storage[storage_id]
                filter_by_storage = FilterDto(field_name="storage", value=storage)
                for product_id in unique_product_ids:
                    product = all_products[product_id]
                    filter_by_product = FilterDto(field_name="product", value=product)
                    filters = [filter_by_storage, filter_by_product]
                    start_values = start_balance_proto.filter_mul(filters).data
                    positive_values = positive_values_proto.filter_mul(filters).data
                    negative_values = negative_values_proto.filter_mul(filters).data
                    remains = product_remains_proto.filter_mul(filters).data

                    item = TurnoverBalanceItem.create(storage, product, product_to_base_unit[product_id])

                    def sum_values(values):
                        return float(sum(map(lambda x: x.value, values)))

                    # Начальное сальдо
                    item.start_balance = sum_values(start_values) + sum_values(remains)
                    # Поступления
                    item.inflows = sum_values(positive_values)
                    # Расходы
                    item.outflows = sum_values(negative_values)

                    result.append(item)

        if include_zero_values:
            filtered_products = Prototype(list(all_products.values())).filter(FilterDto(field_name='id', value=unique_product_ids, op="notin")).data
            for product in filtered_products:
                result.append(TurnoverBalanceItem.create(None, product, product.unit))

        return Prototype(result).filter_mul(dto.result_filters).sort(dto.result_sorts).data

    @staticmethod
    def calculate_remains(new_block_date: datetime, all_transactions: list[TransactionModel], all_products: dict):
        start_date = datetime.fromtimestamp(0)  # timestamp с начала 1970 года
        tbs_items: list[TurnoverBalanceItem] = TurnoverBalanceSheet.calculate(all_transactions, all_products,
                                                                              FilterTbsDto(), start_date,
                                                                              new_block_date, include_zero_values=False)
        remains = {}
        for item in tbs_items:
            model = ProductRemainModel.create(item.inflows + item.outflows, item.unit, item.product, item.storage)
            remains[model.id] = model
        return remains

    @staticmethod
    def change_block_date(new_block_date: datetime, all_transactions: list[TransactionModel], all_products: dict):
        Repository().data[RepoKeys.PRODUCT_REMAINS] = TurnoverBalanceSheet.calculate_remains(new_block_date, all_transactions, all_products)
        SettingsManager().settings.block_date = new_block_date

