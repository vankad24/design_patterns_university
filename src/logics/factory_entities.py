from src.logics.responses.abstract_response import AbstractResponse
from src.logics.responses.csv_response import CsvResponse
from src.logics.responses.json_response import JsonResponse
from src.logics.responses.markdown_response import MarkdownResponse
from src.logics.responses.response_format import ResponseFormat
from src.models.validators.exceptions import OperationException

class FactoryEntities:
    """
    Фабрика, предназначенная для создания (получения) класса,
    ответственного за формирование HTTP-ответа в определенном формате.
    Использует перечисление ResponseFormat для сопоставления с конкретными классами ответов.
    """
    _match = {
        ResponseFormat.CSV: CsvResponse,
        ResponseFormat.JSON: JsonResponse,
        ResponseFormat.MARKDOWN: MarkdownResponse,
    }

    def create(self, r_format: ResponseFormat) -> type[AbstractResponse]:
        """
        Возвращает класс (не экземпляр), который умеет строить ответ
        в заданном формате.

        :param r_format: Требуемый формат ответа из перечисления ResponseFormat.
        :return: Класс, наследующий AbstractResponse.
        :raises OperationException: Если запрошенный формат не поддерживается (отсутствует в _match).
        """
        if r_format not in self._match:
            raise OperationException("Формат неверный")
        # Возвращаем сам класс, который будет вызван позже для построения ответа (например, Class.build(data))
        return self._match[r_format]