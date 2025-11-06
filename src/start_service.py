from src.core.functions import load_json
from src.core.singletone import Singleton
from src.dto.abstract_dto import AbstractDto
from src.dto.functions import create_dto
from src.models.abstract_model import AbstractModel
from src.models.ingridient import IngredientModel
from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.recipe import RecipeModel
from src.models.storage import StorageModel
from src.models.transaction import TransactionModel

from src.repository import Repository, RepoKeys
from src.settings_manager import SettingsManager


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

    def __init__(self, path='./settings.json'):
        """
        Инициализация сервиса:
        - Загружает ссылку на репозиторий.
        - Создаёт пустые словари для хранения созданных моделей по ключам RepoKeys.
        - Устанавливает путь к JSON-файлу с данными.
        """
        self.__loaded_data = None
        self.__filepath = path
        self.__repo = Repository()
        self.__cached_models = {}
        for key in RepoKeys:
            self.__cached_models[str(key)] = {}

        settings = SettingsManager().settings
        if settings.first_start:
            self.start()
            settings.first_start=False

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
        self.__loaded_data = load_json(filepath)[Repository.CONFIG_KEY]

    def start(self):
        """
        Создаёт все стандартные сущности приложения.
        Порядок загрузки важен
        """
        # Загрузка из файла
        self.load(self.__filepath)

        # Массив для перебора (Порядок важен!)
        entities_to_load = [
            (RepoKeys.MEASUREMENT_UNITS, MeasurementUnitModel),
            (RepoKeys.PRODUCT_GROUPS, ProductGroupModel),
            (RepoKeys.PRODUCTS, ProductModel),
            (RepoKeys.INGREDIENTS, IngredientModel),
            (RepoKeys.RECIPES, RecipeModel),
            (RepoKeys.STORAGES, StorageModel),
            (RepoKeys.TRANSACTIONS, TransactionModel),
        ]

        for repo_key, model_class in entities_to_load:
            self.create_models_from_loaded(repo_key, model_class, model_class.DTO_CLASS)