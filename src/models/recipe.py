from src.models.abstract_model import AbstractModel
from src.models.product import ProductModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import validate_val, not_empty


class RecipeModel(AbstractModel):
    def __init__(self):
        super().__init__()

    # Наименование рецепта
    __name: str = ""
    # Состав рецепта: список кортежей (ProductModel, количество)
    __ingredients: list[tuple["ProductModel", float]] = []
    # Пошаговая инструкция
    __guide: str = ""

    # --- Название ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self.__name = value.strip()

        # --- Инструкция ---

    @property
    def guide(self) -> str:
        return self.__guide

    @guide.setter
    @validate_setter(str)
    def guide(self, value: str):
        self.__guide = value.strip()

    # --- Ингредиенты ---
    @property
    def ingredients(self) -> list[tuple["ProductModel", float]]:
        return self.__ingredients

    def add_ingredient(self, product: "ProductModel", amount: float):
        """
        Добавить ингредиент в рецепт.
        :param product: экземпляр ProductModel
        :param amount: количество (например, 100 грамм)
        """
        validate_val(product, ProductModel)
        validate_val(amount, float, check_func=lambda x: x > 0)
        self.__ingredients.append((product, amount))

    def remove_ingredient(self, product: "ProductModel"):
        """
        Удалить ингредиент по ссылке на продукт.
        """
        self.__ingredients = [
            (p, a) for (p, a) in self.__ingredients if p != product
        ]

    def get_total_items(self) -> int:
        """
        Вернуть количество позиций в рецепте.
        """
        return len(self.__ingredients)

    @staticmethod
    def create(name: str, ingredients: list[tuple["ProductModel", float]] = None, guide: str = ""):
        """
        Фабричный метод для создания экземпляра RecipeModel.
        :param name: название рецепта
        :param ingredients: список (ProductModel, количество)
        :param guide: инструкция по приготовлению
        :return: экземпляр RecipeModel
        """
        item = RecipeModel()
        item.name = name
        if ingredients:
            for product, amount in ingredients:
                item.add_ingredient(product, amount)
        if guide:
            item.guide = guide
        return item
