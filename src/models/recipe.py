from src.models.abstract_model import AbstractModel
from src.models.ingridient import IngredientModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import validate_val, not_empty


###############################################
# Модель рецепта
class RecipeModel(AbstractModel):
    # Наименование рецепта
    _name: str = ""
    # Время приготовления
    _cooking_time: str = ""
    # Пошаговая инструкция
    _steps: list[str] = []
    # Состав рецепта — список IngredientModel
    _ingredients: list[IngredientModel] = []

    # --- Наименование ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self._name = value.strip()

    # --- Время приготовления ---
    @property
    def cooking_time(self) -> str:
        return self._cooking_time

    @cooking_time.setter
    @validate_setter(str, check_func=not_empty)
    def cooking_time(self, value: str):
        self._cooking_time = value.strip()

    # --- Пошаговая инструкция ---
    @property
    def steps(self) -> list[str]:
        return self._steps

    @steps.setter
    @validate_setter(list)
    def steps(self, value: list[str]):
        for step in value:
            validate_val(step, str)
        self._steps = value

    # --- Состав ---
    @property
    def ingredients(self) -> list[IngredientModel]:
        return self._ingredients

    @ingredients.setter
    @validate_setter(list)
    def ingredients(self, value: list[IngredientModel]):
        for ing in value:
            validate_val(ing, IngredientModel)
        self._ingredients = value

    # --- Фабричный метод ---
    @staticmethod
    def create(name: str, ingredients: list[IngredientModel] = None, steps: list[str] = None, cooking_time: str = ""):
        """
        Фабричный метод для создания экземпляра RecipeModel.
        :param name: название рецепта
        :param ingredients: список экземпляров IngredientModel
        :param steps: список шагов инструкции
        :param cooking_time: время приготовления
        :return: экземпляр RecipeModel
        """
        item = RecipeModel()
        item.name = name
        if ingredients:
            item.ingredients = ingredients
        if steps:
            item.steps = steps
        if cooking_time:
            item.cooking_time = cooking_time
        return item
