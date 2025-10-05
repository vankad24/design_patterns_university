import os.path
import uuid

from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.recipe import RecipeModel
from src.models.storage import StorageModel
from src.models.validators.exceptions import ArgumentException
from src.settings_manager import SettingsManager
from src.models.company import CompanyModel

import pytest

class TestModels:
    """
    Класс с тестами для моделей
    """

    def test_create_model_empty_company_model(self):
        """
        Проверяет создание CompanyModel без установки данных.
        После создания все поля должны быть пустыми.
        """
        model = CompanyModel()
        # Действие

        # Проверки
        assert model.name == ""

    def test_create_model_not_empty_company_model(self):
        """
        Проверяет создание CompanyModel с последующей установкой данных.
        После установки поле name не должно быть пустым.
        """
        model = CompanyModel()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    def test_load_company_model(self):
        """
        Проверяет загрузку данных CompanyModel из JSON файла через SettingsManager.
        Проверяется корректность имени компании после загрузки.
        """
        file_name = '../settings.json'
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True
        assert manager.settings.company.name == 'Рога и копыта'

    def test_load_company_model_abs_path(self):
        """
        Проверяет загрузку данных CompanyModel из JSON файла по абсолютному пути.
        """
        file_name = os.path.abspath('../settings.json')
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True
        assert manager.settings.company.name == 'Рога и копыта'

    def test_load_model_company_model_from_same_file(self):
        """
        Проверяет работу Singleton при загрузке CompanyModel из одного и того же файла.
        Ожидается, что два менеджера будут использовать один и тот же объект company.
        """
        file_name = '../settings.json'
        manager = SettingsManager()
        manager.file_name = file_name
        manager2 = SettingsManager()

        # Действие
        manager.load()
        manager2.load()

        # Проверки
        assert manager.settings.company == manager2.settings.company

    def test_load_from_dict_company(self):
        """
        Проверяет загрузку данных в CompanyModel из словаря.
        Все поля должны быть установлены согласно словарю.
        """
        data = {
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001"
        }
        company = CompanyModel()

        # Действие
        company.load_from_dict(data)

        # Проверки
        assert company.name == data["name"]
        assert company.inn == data["inn"]
        assert company.account == data["account"]
        assert company.corr_account == data["corr_account"]
        assert company.bik == data["bik"]
        assert company.ownership == data["ownership"]

    def test_load_from_dict_company_from_dir(self):
        """
        Проверяет загрузку CompanyModel из JSON файла, расположенного в тестовой директории.
        Проверяется корректность всех полей компании после загрузки.
        """
        data = {
            "name": "ООО Тестовая Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00002"
        }
        file_name = './test_company.json'
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        manager.load()
        company = manager.settings.company

        # Проверки
        assert company.name == data["name"]
        assert company.inn == data["inn"]
        assert company.account == data["account"]
        assert company.corr_account == data["corr_account"]
        assert company.bik == data["bik"]
        assert company.ownership == data["ownership"]

    def test_load_from_dict_exception_wrong_arg(self):
        """
        Проверяет обработку ошибок при загрузке CompanyModel из некорректного аргумента.
        Ожидается выброс ArgumentException при None или неправильном типе данных.
        """
        company = CompanyModel()
        with pytest.raises(ArgumentException) as exc_info:
            company.load_from_dict(None)
        assert exc_info.value.args[0] == "Пустой аргумент"

        with pytest.raises(ArgumentException) as exc_info:
            company.load_from_dict(["name"])
        assert exc_info.value.args[0].startswith("Некорректный тип")

    # Параметры для тестирования некорректных значений полей компании
    @pytest.mark.parametrize(
        "field, value, error_msg",
        [
            ("name", "   ", "не прошёл проверку проверочной функцией"),
            ("inn", "123", "Некорректная длина аргумента"),
            ("inn", "123456789012435", "Некорректная длина аргумента"),
            ("inn", "12345678901a", "не прошёл проверку проверочной функцией"),
            ("account", "123", "Некорректная длина аргумента"),
            ("account", "1234567890a", "не прошёл проверку проверочной функцией"),
            ("corr_account", "123", "Некорректная длина аргумента"),
            ("corr_account", "1234567890a", "не прошёл проверку проверочной функцией"),
            ("bik", "123", "Некорректная длина аргумента"),
            ("bik", "12345678a", "не прошёл проверку проверочной функцией"),
            ("ownership", "1234", "Некорректная длина аргумента"),
            ("ownership", "abda", "Некорректная длина аргумента"),
            ("ownership", "1234a234ds", "Некорректная длина аргумента"),
        ]
    )
    def test_load_from_dict_exception_incorrect_fields(self, field, value, error_msg):
        """
        Тестирует загрузку данных в CompanyModel с некорректными значениями полей.
        Проверяет, что при неверных данных выбрасывается RuntimeError с правильной причиной.
        """
        data = {
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001",
            field: value
        }

        company = CompanyModel()

        with pytest.raises(RuntimeError) as exc_info:
            company.load_from_dict(data)

        assert exc_info.value.args[0] == f"Setter '{field}' не выполнился"
        caused_exc = exc_info.value.__cause__
        assert isinstance(caused_exc, ArgumentException)
        assert error_msg in caused_exc.args[0]

    def test_equals_storage_models_creation(self):
        """
        Проверяет, что два StorageModel с одинаковым id считаются равными.
        """
        myid = uuid.uuid4().hex
        storage1 = StorageModel()
        storage2 = StorageModel()
        storage1.id = myid
        storage2.id = myid

        assert storage1 == storage2

    def test_not_equals_storage_models_creation(self):
        """
        Проверяет, что два StorageModel с разными id считаются не равными.
        """
        storage1 = StorageModel()
        storage2 = StorageModel()

        assert storage1 != storage2

    def test_storage_model_creation(self):
        """
        Проверяет создание StorageModel и корректность установки атрибутов.
        """
        storage = StorageModel()
        storage.name = "Основной склад"
        storage.address = "г. Москва, ул. Ленина, 1"

        assert storage.name == "Основной склад"
        assert storage.address == "г. Москва, ул. Ленина, 1"

    def test_measurement_unit_creation(self):
        """
        Проверяет создание единиц измерения и правильность установки базовой единицы.
        """
        gram = MeasurementUnitModel("грамм", 1.0)
        kg = MeasurementUnitModel("кг", 1000.0, gram)

        assert gram.base_unit == gram
        assert kg.base_unit == gram

    def test_convert_measurement_unit_chain_conversion(self):
        """
        Проверяет корректность цепочки конверсий между единицами измерения.
        """
        gram = MeasurementUnitModel("грамм", 1.0)
        kg = MeasurementUnitModel("кг", 1000.0, gram)
        ton = MeasurementUnitModel("т", 1000.0, kg)

        assert ton.convert_to(2, gram) == 2_000_000
        assert kg.convert_to(5, gram) == 5000
        assert ton.convert_to(1, kg) == 1000
        assert kg.convert_to(5, kg) == 5
        assert gram.convert_to(2, gram) == 2

    def test_product_group_and_product_creation(self):
        """
        Проверяет создание ProductGroupModel и ProductModel,
        включая корректную установку всех атрибутов.
        """
        group = ProductGroupModel()
        group.name = "Молочные продукты"

        long_name = "a" * 50
        long_full_name = "a" * 255

        unit = MeasurementUnitModel("шт", 1.0)
        product = ProductModel()
        product.code = "P001"
        product.name = long_name
        product.full_name = long_full_name
        product.unit = unit
        product.group = group
        product.price = 75.5

        assert product.code == "P001"
        assert product.name == long_name
        assert product.full_name == long_full_name
        assert product.unit == unit
        assert product.group == group
        assert product.price == 75.5

    def test_setter_product_model_exception_too_long_string(self):
        """
        Проверяет, что при установке слишком длинных строк в ProductModel выбрасывается RuntimeError.
        """
        product = ProductModel()
        long_name = "a" * 51
        long_full_name = "a" * 256

        with pytest.raises(RuntimeError) as exc_info:
            product.name = long_name

        with pytest.raises(RuntimeError) as exc_info:
            product.full_name = long_full_name

    def test_recipe_create_model(self):
        """
        Проверяет фабричный метод create для RecipeModel.
        """
        group = ProductGroupModel.create("Продукты питания")
        unit_g = MeasurementUnitModel.create("грамм")
        flour = ProductModel.create("Мука", "Пшеничная мука", unit_g, group)

        ingredients = [(flour, 200.0)]
        recipe = RecipeModel.create("Тесто", ingredients)

        assert recipe.name == "Тесто"
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0] == (flour, 200.0)

    def test_recipe_creation_and_ingredients(self):
        """
        Проверяет создание RecipeModel и корректность добавления ингредиентов.
        """
        # Создание группы и продуктов
        group = ProductGroupModel()
        group.name = "Продукты питания"

        unit_g = MeasurementUnitModel("грамм", 1.0)
        unit_piece = MeasurementUnitModel("шт", 1.0)

        flour = ProductModel()
        flour.name = "Мука"
        flour.full_name = "Пшеничная мука"
        flour.unit = unit_g
        flour.group = group

        egg = ProductModel()
        egg.name = "Яйцо"
        egg.full_name = "Куриное яйцо"
        egg.unit = unit_piece
        egg.group = group

        # Создание рецепта
        recipe = RecipeModel()
        recipe.name = "Блинчики"
        recipe.add_ingredient(flour, 100.0)
        recipe.add_ingredient(egg, 2.0)

        assert recipe.name == "Блинчики"
        assert len(recipe.ingredients) == 2
        assert recipe.ingredients[0] == (flour, 100.0)
        assert recipe.ingredients[1] == (egg, 2.0)

    def test_add_ingredient_invalid_values(self):
        """
        Проверяет, что при добавлении неверных типов или отрицательного количества выбрасывается исключение.
        """
        recipe = RecipeModel.create("Тестовый рецепт")
        product = ProductModel.create("Мука", "Мука пшеничная", MeasurementUnitModel.create("грамм"),
                                      ProductGroupModel.create("Продукты"))

        # Неверный тип продукта
        with pytest.raises(ArgumentException):
            recipe.add_ingredient("not a product", 100.0)

        # Неверный тип количества
        with pytest.raises(ArgumentException):
            recipe.add_ingredient(product, "100")

        # Отрицательное количество
        with pytest.raises(ArgumentException):
            recipe.add_ingredient(product, -50.0)

    def test_remove_ingredient(self):
        """
        Проверяет корректное удаление ингредиента из рецепта.
        """
        group = ProductGroupModel.create("Продукты")
        unit = MeasurementUnitModel.create("грамм")
        flour = ProductModel.create("Мука", "Мука пшеничная", unit, group)
        sugar = ProductModel.create("Сахар", "Сахар белый", unit, group)

        recipe = RecipeModel.create("Тесто", [(flour, 100.0), (sugar, 50.0)])
        recipe.remove_ingredient(flour)

        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0][0] == sugar

if __name__ == "__main__":
    pytest.main(['-v'])