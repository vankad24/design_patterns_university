import connexion
from flask import request

from src.core.functions import dump_json
from src.core.prototype import Prototype
from src.dto.filter_dto import FilterDto
from src.dto.filter_models_dto import FilterModelsDto
from src.dto.filter_tbs_dto import FilterTbsDto
from src.dto.functions import create_dto
from src.export_manager import ExportManager
from src.logics.factory_converters import FactoryConverters
from src.logics.factory_entities import FactoryEntities
from src.logics.responses.error_response import ErrorResponse
from src.logics.responses.json_response import JsonResponse
from src.logics.responses.response_format import ResponseFormat
from src.logics.turnover_balance_sheet import TurnoverBalanceSheet
from src.repository import RepoKeys, Repository
from src.settings_manager import SettingsManager
from src.start_service import StartService

start_service = StartService()
repository = Repository()
settings_manager = SettingsManager()

app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml', base_path='/api')
# Ссылка на документацию
# http://127.0.0.1:8080/api/ui/

@app.route("/api/status", methods=['GET'])
def status():
    """
        Проверить доступность REST API
    """
    return "SUCCESS"


@app.route("/api/responses/formats", methods=['GET'])
def responses_formats():
    """
    Получить доступные форматы ответа
    """
    return JsonResponse.build([str(v) for v in ResponseFormat])

@app.route("/api/responses/models", methods=['GET'])
def responses_models():
    """
    Получить доступные модели (типы данных) для ответа
    """
    return JsonResponse.build([str(v) for v in RepoKeys])

@app.route("/api/responses/build", methods=['GET'])
def build_response():
    """
    Сформировать ответ по заданной модели и формату
    """
    try:
        f = ResponseFormat(request.args.get('format'))
    except Exception as e:
        return ErrorResponse.build("неверный аргумент 'format'")

    try:
        model = RepoKeys(request.args.get('model'))
    except Exception as e:
        return ErrorResponse.build("неверный аргумент 'model'")

    models = list(repository.data[model].values())
    result = FactoryEntities().create(f).build(models)
    return result


@app.route("/api/recipes", methods=['GET'])
def get_recipes():
    """
    Получить список всех рецептов
    """
    recipes = list(repository.data[RepoKeys.RECIPES].values())
    result = FactoryConverters.convert(recipes)
    return JsonResponse.build(result)

@app.route("/api/recipes/<recipe_id>", methods=['GET'])
def get_recipe(recipe_id: str):
    """
    Получить конкретный рецепт по ID
    """
    try:
        recipe = repository.data[RepoKeys.RECIPES][recipe_id]
    except Exception as e:
        return ErrorResponse.build(f"не найден рецепт с id: {recipe_id}")

    result = FactoryConverters.convert(recipe)
    return JsonResponse.build(result)

# Пример http://127.0.0.1:8080/api/tbs/7dc27e96-e6ad-4e5e-8c56-84e00667e3d7?start_date=2025-01-02&end_date=2025-02-01
@app.route("/api/tbs/<storage_id>", methods=['GET'])
def get_tbs(storage_id: str):
    """
    Оборотно-сальдовая ведомость (Turnover balance sheet)
    - `storage_id`: уникальный код склада
    - `start_date`: начальная дата отчёта
    - `end_date`: дата окончания отчёта
    """

    storage = start_service.repo.data[RepoKeys.STORAGES].get(storage_id)
    if storage is None:
        return ErrorResponse.build(f"Склад с id:'{storage_id}' не найден")

    dto = FilterTbsDto(transaction_filters=[FilterDto(field_name="storage", value=storage)],
                       start_date=request.args.get('start_date'), end_date=request.args.get('end_date'))

    if dto.start_date >= dto.end_date:
        return ErrorResponse.build(f"Конечная дата не может быть раньше начальной")

    try:
        items = TurnoverBalanceSheet.calculate(
            repository.get_values(RepoKeys.TRANSACTIONS),
            repository.data[RepoKeys.PRODUCTS],
            dto)
    except Exception as e:
        return ErrorResponse.build(f"Ошибка во время обработки данных: {e}")

    return FactoryEntities().create(ResponseFormat.JSON).build(items)

@app.route("/api/repository/all", methods=['POST', 'GET'])
def get_all_from_repository():
    """
    Получить все данные из Repository в формате JSON
    """
    data = FactoryConverters.convert(repository.data)
    return JsonResponse.build(data)

@app.route("/api/save_all", methods=['POST', 'GET'])
def save_all():
    """
    Сохранить все данные (settings и repository) в файл
    """
    exported_dict = ExportManager().export_to_dict()
    data = FactoryConverters.convert(exported_dict)
    dump_json(data, settings_manager.file_name)
    return JsonResponse.build([{"status":"ok"}])

@app.route("/api/tbs-filter", methods=['POST'])
def get_tbs_filter():
    """
    Оборотно-сальдовая ведомость (Turnover balance sheet)
    """
    try:
        dto: FilterTbsDto = create_dto(FilterTbsDto, request.get_json())
    except Exception as e:
        return ErrorResponse.build(f"Ошибка в переданных аргументах: {e}")

    if dto.start_date >= dto.end_date:
        return ErrorResponse.build(f"Конечная дата не может быть раньше начальной")

    try:
        items = TurnoverBalanceSheet.calculate(
            repository.get_values(RepoKeys.TRANSACTIONS),
            repository.data[RepoKeys.PRODUCTS],
            dto)
    except Exception as e:
        return ErrorResponse.build(f"Ошибка во время обработки данных: {e}")

    return FactoryEntities().create(ResponseFormat.JSON).build(items)

@app.route("/api/models-filter", methods=['POST'])
def get_models_filter():
    """
    Получить модели и отфильтровать их
    """
    try:
        dto: FilterModelsDto = create_dto(FilterModelsDto, request.get_json())
    except Exception as e:
        return ErrorResponse.build(f"Ошибка в переданных аргументах: {e}")
    try:
        model = RepoKeys(dto.model)
    except:
        return ErrorResponse.build(f"Неверный аргумент 'model':{dto.model}")

    models = Prototype(repository.get_values(model)).filter_mul(dto.filters).sort(dto.sorts).data
    return FactoryEntities().create(ResponseFormat.JSON).build(models)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
