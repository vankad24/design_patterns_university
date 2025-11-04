from src.core.functions import load_json
from src.core.singletone import Singleton
from src.dto.abstract_dto import AbstractDto
from src.dto.functions import create_dto
from src.dto.ingridient_dto import IngredientDto
from src.dto.measurement_dto import MeasurementUnitDto
from src.dto.product_dto import ProductDto
from src.dto.product_group_dto import ProductGroupDto
from src.dto.recipe_dto import RecipeDto
from src.dto.storage_dto import StorageDto
from src.dto.transaction_dto import TransactionDto
from src.models.abstract_model import AbstractModel
from src.models.ingridient import IngredientModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.recipe import RecipeModel
from src.models.storage import StorageModel
from src.models.transaction import TransactionModel
from src.models.validators.functions import validate_val

from src.repository import Repository, RepoKeys

class StartService(metaclass=Singleton):
    """
    Сервис для инициализации базовых данных приложения:
    - Единицы измерения
    - Группы номенклатуры
    - Продукты
    - Ингредиенты
    - Рецепты

    Использует Singleton, чтобы существовал только один экземпляр сервиса.
    """

    __cached_models: dict
    __repo: Repository

    def __init__(self):
        """
        Инициализация сервиса:
        - Загружает ссылку на репозиторий.
        - Создаёт пустые словари для хранения созданных моделей по ключам RepoKeys.
        - Устанавливает путь к JSON-файлу с данными.
        """
        self.__loaded_data = None
        self.__filepath = './settings.json'
        self.__repo = Repository()
        self.__cached_models = {}
        for key in RepoKeys:
            self.__cached_models[str(key)] = {}

    def set_path(self, path):
        validate_val(path, str)
        self.__filepath = path

    # --- Репозиторий ---
    @property
    def repo(self):
        """
        Возвращает объект репозитория.
        Используется для доступа к загруженным моделям по ключам RepoKeys.
        """
        return self.__repo

    def create_models_from_loaded(self, key: RepoKeys, model_type, dto_type):
        """
        Создаёт модели заданного типа из ранее загруженных данных JSON
        и сохраняет их в created_models и репозитории.

        :param key: ключ из RepoKeys, определяющий тип данных
        :param model_type: класс Model, которая будет создана (наследник AbstractModel)
        :param dto_type: класс Dto, которая будет создана (наследник AbstractDto)
        """
        for data in self.__loaded_data[key]:
            dto: AbstractDto = create_dto(dto_type, data)
            if dto.id in self.__cached_models:
                continue
            model: AbstractModel = model_type.from_dto(dto, self.__cached_models)
            self.__cached_models[model.id] = model
            self.repo.data[key][model.id] = model

    def load(self, filepath):
        """
        Загружает данные из JSON-файла и сохраняет их во внутреннее поле __loaded_data.

        :param filepath: путь к JSON-файлу
        """
        self.__loaded_data = load_json(filepath)

    def start(self):
        """
        Создаёт все стандартные сущности приложения.
        Порядок загрузки важен
        """
        # Не менять порядок
        self.load(self.__filepath)
        self.create_models_from_loaded(RepoKeys.MEASUREMENT_UNITS, MeasurementUnitModel, MeasurementUnitDto)
        self.create_models_from_loaded(RepoKeys.PRODUCT_GROUPS, ProductGroupModel, ProductGroupDto)
        self.create_models_from_loaded(RepoKeys.PRODUCTS, ProductModel, ProductDto)
        self.create_models_from_loaded(RepoKeys.INGREDIENTS, IngredientModel, IngredientDto)
        self.create_models_from_loaded(RepoKeys.RECIPES, RecipeModel, RecipeDto)
        self.create_models_from_loaded(RepoKeys.STORAGES, StorageModel, StorageDto)
        self.create_models_from_loaded(RepoKeys.TRANSACTIONS, TransactionModel, TransactionDto)
