from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.recipe import RecipeModel
from src.repository import Repository


class StartService:
    """
    Сервис инициализации базовых данных:
    - единицы измерения
    - группы номенклатуры
    - продукты
    - рецепты
    """

    __measurement_units = {}
    __products = {}
    __product_groups = {}
    __recipes = {}

    __repo: Repository

    def __init__(self):
        self.__repo = Repository()

    # --- Репозиторий ---
    @property
    def repo(self):
        return self.__repo

    # --- ЕДИНИЦЫ ИЗМЕРЕНИЯ ---
    def add_unit(self, name, base=None, factor=1.0):
        """
        Добавить единицу измерения.
        :param name: название единицы (например, "грамм", "кг")
        :param base: базовая единица измерения
        :param factor: коэффициент пересчёта к базовой
        """
        unit = MeasurementUnitModel.create(name, base, factor)
        self.__measurement_units[name] = unit
        self.__repo.measurement_units.append(unit)
        return unit

    # --- ГРУППЫ НОМЕНКЛАТУРЫ ---
    def add_product_group(self, name):
        """
        Добавить группу товаров.
        :param name: название группы
        """
        group = ProductGroupModel.create(name)
        self.__product_groups[name] = group
        self.__repo.product_groups.append(group)
        return group

    def add_product(self, name, full_name="", unit=None, group=None):
        """
        Добавить продукт.
        :param name: краткое название
        :param full_name: полное название
        :param unit: единица измерения (MeasurementUnitModel)
        :param group: группа продукта (ProductGroupModel)
        """
        product = ProductModel.create(name, full_name, unit, group)
        self.__products[name] = product
        self.__repo.products.append(product)
        return product

    def add_recipe(self, name, ingredients):
        """
        Добавить рецепт.
        :param name: название рецепта
        :param ingredients: список кортежей (ProductModel, количество)
        """
        recipe = RecipeModel.create(name, ingredients)
        self.__recipes[name] = recipe
        self.__repo.recipes.append(recipe)
        return recipe

    def default_create_measurement_unit(self):
        """
        Создать стандартные единицы измерения.
        """
        g = self.add_unit("грамм")
        kg = self.add_unit("кг", g, 1000.0)
        ton = self.add_unit("т", kg, 1000.0)
        piece = self.add_unit("шт")

    def default_create_product_groups(self):
        """
        Создать стандартные группы номенклатуры.
        """
        food = self.add_product_group("Продукты питания")
        spices = self.add_product_group("Специи")

    def default_create_products(self):
        """
        Создать стандартные продукты.
        """
        g = self.__measurement_units.get("грамм")
        piece = self.__measurement_units.get("шт")
        food = self.__product_groups.get("Продукты питания")
        spices = self.__product_groups.get("Специи")

        flour = self.add_product("Пшеничная мука", "Мука пшеничная высшего сорта", g, food)
        sugar = self.add_product("Сахар", "Сахар белый", g, food)
        butter = self.add_product("Сливочное масло", "Масло сливочное 82,5%", g, food)
        egg = self.add_product("Яйцо", "Куриное яйцо", piece, food)
        vanilla = self.add_product("Ванилин", "Ванилин кристаллический", g, spices)

    def default_create_recipes(self):
        """
        Создать стандартные рецепты.
        """
        flour = self.__products.get("Пшеничная мука")
        sugar = self.__products.get("Сахар")
        butter = self.__products.get("Сливочное масло")
        egg = self.__products.get("Яйцо")
        vanilla = self.__products.get("Ванилин")

        waffles = self.add_recipe("Вафли хрустящие в вафельнице", [
            (flour, 100.0),
            (sugar, 80.0),
            (butter, 70.0),
            (egg, 1.0),
            (vanilla, 5.0)
        ])

    def start(self):
        """
        Создать все стандартные сущности.
        """
        self.default_create_measurement_unit()
        self.default_create_product_groups()
        self.default_create_products()
        self.default_create_recipes()
