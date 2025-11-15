import operator
import re

from src.core.functions import get_nested_attr
from src.dto.filter_dto import FilterDto
from src.dto.sorting_dto import SortingDto
from src.models.validators.functions import validate_val

# Класс - прототип
class Prototype:
    """
    Базовый класс 'Прототип', предназначенный для работы с коллекцией данных (списком).
    Он реализует паттерн "Прототип" для создания копий самого себя (клон)
    и предоставляет методы для фильтрации и сортировки данных.
    """
    _data: list = []  # Защищенное поле для хранения исходного набора данных.

    _operator_to_func = {
        # Словарь, сопоставляющий строковые операторы с соответствующими функциями
        # из модуля 'operator' или лямбда-функциями для выполнения сравнений и логических операций.
        "==": operator.eq,  # Равно
        "!=": operator.ne,  # Не равно
        "<": operator.lt,  # Меньше
        "<=": operator.le,  # Меньше или равно
        ">": operator.gt,  # Больше
        ">=": operator.ge,  # Больше или равно
        # Дополнительно:
        "in": operator.contains,  # Проверяет, содержится ли левый операнд в правом итерируемом объекте (x in iterable)
        "notin": lambda x, y: x not in y,  # Проверяет, не содержится ли левый операнд в правом
        "contains": lambda x, y: y in x,  # Проверяет, содержится ли правый операнд в левом (iterable contains y)
        "notcontains": lambda x, y: y not in x,  # Проверяет, не содержится ли правый операнд в левом
        "and": operator.and_,  # Побитовое И
        "or": operator.or_,  # Побитовое ИЛИ
        "xor": operator.xor,  # Побитовое исключающее ИЛИ
        "like": lambda s, pattern: bool(re.fullmatch(pattern, s)) # Сравнение строки с регулярным выражением (полное совпадение)
    }

    # Набор данных
    @property
    def data(self):
        """
        Свойство (getter), предоставляющее доступ к текущему набору данных (_data).
        """
        return self._data

    def __init__(self, data: list):
        """
        Конструктор класса. Инициализирует Прототип заданным списком данных.

        :param data: Список элементов, с которым будет работать Прототип.
        """
        validate_val(data, list)
        self._data = data

    def clone(self, data: list = None) -> "Prototype":
        """
        Создает новый экземпляр класса Prototype (клон текущего объекта).

        :param data: Опциональный новый список данных для клона. Если None,
                     используются данные текущего экземпляра.
        :return: Новый экземпляр Prototype.
        """
        inner_data = self._data if data is None else data
        instance = Prototype(inner_data)
        return instance

    # Универсальная функция фильтрации с поддержкой вложенных структур
    def filter(self, dto: FilterDto) -> "Prototype":
        """
        Фильтрует текущий набор данных на основе одного критерия, заданного в DTO.
        Поддерживает доступ к вложенным атрибутам с помощью синтаксиса "точка" (e.g., 'field.subfield').

        :param dto: Объект FilterDto, содержащий имя поля (с точками), оператор и значение.
        :return: Новый экземпляр Prototype, содержащий только отфильтрованные данные.
        """
        # Фильтрация с использованием соответствующей функции оператора и получения вложенного атрибута
        result = filter(lambda item: self._operator_to_func[dto.op](get_nested_attr(item, dto.field_name.split(".")), dto.value), self.data)
        return self.clone(list(result))

    def filter_mul(self, dtos: list[FilterDto]) -> "Prototype":
        """
        Последовательно применяет несколько критериев фильтрации к набору данных.
        Каждый последующий фильтр применяется к результату предыдущего (логическое И).

        :param dtos: Список объектов FilterDto, каждый из которых представляет критерий фильтрации.
        :return: Новый экземпляр Prototype с данными, прошедшими все фильтры.
        """
        result = self
        for dto in dtos:
            result = result.filter(dto)
        return result

    def sort(self, dto: SortingDto):
        """
        Сортирует текущий набор данных на основе заданных критериев сортировки.
        Поддерживает сортировку по нескольким полям и по вложенным атрибутам.

        :param dto: Объект SortingDto, содержащий список имен полей для сортировки
                    и флаг направления (descending).
        :return: Новый экземпляр Prototype, содержащий отсортированные данные.
                 Возвращает себя, если DTO отсутствует.
        """
        if not dto:
            return self
        # Сортировка с использованием списка ключей (для многоуровневой сортировки)
        return self.clone(sorted(self._data, key=lambda item: [get_nested_attr(item, field.split(".")) for field in dto.field_names], reverse=dto.descending))