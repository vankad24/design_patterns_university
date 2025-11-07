from datetime import datetime

import connexion
from flask import request

from src.core.functions import dump_json
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
    return JsonResponse.build([str(v) for v in ResponseFormat])

@app.route("/api/responses/models", methods=['GET'])
def responses_models():
    return JsonResponse.build([str(v) for v in RepoKeys])

@app.route("/api/responses/build", methods=['GET'])
def build_response():
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
    recipes = list(repository.data[RepoKeys.RECIPES].values())
    result = FactoryConverters.convert(recipes)
    return JsonResponse.build(result)

@app.route("/api/recipes/<recipe_id>", methods=['GET'])
def get_recipe(recipe_id: str):
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
    start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

    storage = start_service.repo.data[RepoKeys.STORAGES].get(storage_id)
    if storage is None:
        return ErrorResponse.build(f"Склад с id:'{storage_id}' не найден")

    if start_date >= end_date:
        return ErrorResponse.build(f"Конечная дата не может быть раньше начальной")

    items = TurnoverBalanceSheet.calculate(repository.data[RepoKeys.TRANSACTIONS].values(), repository.data[RepoKeys.PRODUCTS], storage, start_date, end_date)

    return FactoryEntities().create(ResponseFormat.JSON).build(items)

@app.route("/api/repository/all", methods=['POST', 'GET'])
def get_all_from_repository():
    """
    JSON со всеми данными из Repository
    """
    data = FactoryConverters.convert(repository.data)
    return JsonResponse.build(data)

@app.route("/api/save_all", methods=['POST', 'GET'])
def save_all():
    """
    Сохранить все данныые в файл
    """
    dicts = [
        settings_manager.dump(),
        repository.dump()
    ]
    dumped_dict = {}
    for d in dicts:
        dumped_dict.update(d)
    data = FactoryConverters.convert(dumped_dict)
    dump_json(data, settings_manager.file_name)
    return JsonResponse.build([{"status":"ok"}])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
