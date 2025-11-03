import connexion
from flask import request

from src.logics.factory_converters import FactoryConverters
from src.logics.factory_entities import FactoryEntities
from src.logics.responses.error_response import ErrorResponse
from src.logics.responses.json_response import JsonResponse
from src.logics.responses.response_format import ResponseFormat
from src.repository import RepoKeys, Repository
from src.start_service import StartService

start_service = StartService()
start_service.start()
repository = Repository()

app = connexion.FlaskApp(__name__)

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
