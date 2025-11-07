from enum import StrEnum


class ResponseFormat(StrEnum):
    """
    Перечисление (Enum), определяющее поддерживаемые форматы для выходных данных (ответов API).
    Использует StrEnum, чтобы значениями элементов были строки (строковые константы).
    """

    CSV = 'csv'
    EXCEL = 'excel'
    JSON = 'json'
    MARKDOWN = 'markdown'
