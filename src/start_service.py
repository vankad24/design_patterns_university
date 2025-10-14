from src.core.functions import load_json
from src.core.singletone import Singleton
from src.models.abstract_model import AbstractModel
from src.models.ingridient import IngredientModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.recipe import RecipeModel
from src.models.utils import model_loader
from src.repository import Repository, RepoKeys


class StartService(metaclass=Singleton):
    """
    Сервис инициализации базовых данных:
    - единицы измерения
    - группы номенклатуры
    - продукты
    - рецепты
    """

    __created_models: dict
    __repo: Repository

    def __init__(self):
        self.__loaded_data = None
        self.__filepath = '../settings.json'
        self.__repo = Repository()
        self.__created_models = {}
        for key in RepoKeys:
            self.__created_models[str(key)] = {}

    # --- Репозиторий ---
    @property
    def repo(self):
        return self.__repo

    def create_models_from_loaded(self, key: RepoKeys, model_type):
        for item in self.__loaded_data[key]:
            model: AbstractModel = model_type()
            model_loader.load_from_dict(model, item, self.__created_models)
            self.__created_models[model.id] = model
            self.repo.data[key][model.id] = model

    def load(self, filepath):
        self.__loaded_data = load_json(filepath)

    def start(self):
        """
        Создать все стандартные сущности.
        """
        # Не менять порядок
        self.load(self.__filepath)
        self.create_models_from_loaded(RepoKeys.MEASUREMENT_UNITS, MeasurementUnitModel)
        self.create_models_from_loaded(RepoKeys.PRODUCT_GROUPS, ProductGroupModel)
        self.create_models_from_loaded(RepoKeys.PRODUCTS, ProductModel)
        self.create_models_from_loaded(RepoKeys.INGREDIENTS, IngredientModel)
        self.create_models_from_loaded(RepoKeys.RECIPES, RecipeModel)
