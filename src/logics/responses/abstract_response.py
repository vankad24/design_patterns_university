from src.models.validators.functions import validate_val

from abc import ABC
from abc import ABC

from src.models.validators.functions import validate_val


class AbstractResponse(ABC):
    """
    Абстрактный базовый класс для всех классов, формирующих HTTP-ответы.
    Требует реализации метода 'build' в классах-наследниках.
    Наследуется от ABC для обеспечения абстрактности.
    """

    @classmethod
    def build(cls, data: list) -> str:
        """
        Абстрактный метод для построения тела HTTP-ответа из переданных данных.
        Должен быть реализован в классах-наследниках для форматирования данных (например, в JSON, XML и т.д.).

        :param data: Список данных, которые необходимо включить в ответ.
        :raises Exception: Если 'data' не является списком или пуст (проверяется 'validate_val').
        :return: Строка, представляющая отформатированный HTTP-ответ.
        """
        validate_val(data, list, check_func=lambda x:len(x)>0)

        return ""


