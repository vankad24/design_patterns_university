import os.path
import shutil
import tempfile
import uuid
from dataclasses import dataclass, field

from src.dto.abstract_dto import AbstractDto
from src.dto.cached_id import CachedId
from src.dto.company_dto import CompanyDto
from src.dto.functions import create_dto
from src.dto.measurement_dto import MeasurementUnitDto
from src.models.abstract_model import AbstractModel
from src.models.ingridient import IngredientModel
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
        file_name = 'test_settings.json'
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        manager.load()

        # Проверки
        assert manager.settings.company.name == 'ООО Тестовая Ромашка'

    def test_load_company_model_abs_path(self):
        """
        Проверяет загрузку данных CompanyModel из JSON файла по абсолютному пути.
        """
        file_name = os.path.abspath('test_settings.json')
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        manager.load()

        # Проверки
        assert manager.settings.company.name == 'ООО Тестовая Ромашка'

    def test_load_company_exception_file_not_found(self):
        """
        Проверяет обработку ошибок при загрузке JSON файла через SettingsManager,
        используя временную копию файла, а затем удаляя ее для проверки ошибки.
        """
        file_name = os.path.abspath('test_settings.json')
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfile(file_name, tmp_file.name)
            file_name = tmp_file.name
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        os.remove(file_name)

        # Проверки
        with pytest.raises(FileNotFoundError) as exc_info:
            manager.load()
        with pytest.raises(FileNotFoundError) as exc_info:
            manager.file_name = file_name


    def test_load_model_company_model_from_same_file(self):
        """
        Проверяет работу Singleton при загрузке CompanyModel из одного и того же файла.
        Ожидается, что два менеджера будут использовать один и тот же объект company.
        """
        file_name = 'test_settings.json'
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
            "id": "c4546e8b-7260-4db8-a673-c8c123ab14a7",
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001"
        }

        # Действие
        company = CompanyModel.from_dto(create_dto(CompanyDto, data), {})

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
        file_name = 'test_settings.json'
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

        with pytest.raises(ArgumentException) as exc_info:
            company = CompanyModel.from_dto(create_dto(CompanyDto, None), {})
        assert exc_info.value.args[0] == "Пустой аргумент"

        with pytest.raises(ArgumentException) as exc_info:
            company = CompanyModel.from_dto(create_dto(CompanyDto, ["name"]), {})
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
            "id": "c4546e8b-7260-4db8-a673-c8c123ab14a7",
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001",
            field: value
        }

        with pytest.raises(RuntimeError) as exc_info:
            company = CompanyModel.from_dto(create_dto(CompanyDto, data), {})

        assert exc_info.value.args[0] == f"Setter '{field}' не выполнился"
        caused_exc = exc_info.value.__cause__
        assert isinstance(caused_exc, ArgumentException)
        assert error_msg in caused_exc.args[0]

    def test_equals_storage_models_creation(self):
        """
        Проверяет, что два StorageModel с одинаковым id считаются равными.
        """
        myid = str(uuid.uuid4())
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

        ingredients = [IngredientModel.create(flour, 200.0, unit_g)]
        recipe = RecipeModel.create("Тесто", ingredients)

        assert recipe.name == "Тесто"
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].product == flour
        assert recipe.ingredients[0].amount == 200.0
        assert recipe.ingredients[0].unit == unit_g

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

        ingredients = [
            IngredientModel.create(flour, 100.0, unit_g),
            IngredientModel.create(egg, 2.0, unit_piece),
        ]

        # Создание рецепта
        recipe = RecipeModel()
        recipe.name = "Блинчики"
        recipe.ingredients = ingredients

        assert recipe.name == "Блинчики"
        assert len(recipe.ingredients) == 2
        assert recipe.ingredients[0].product == flour
        assert recipe.ingredients[0].amount == 100.0
        assert recipe.ingredients[0].unit == unit_g
        assert recipe.ingredients[1].product == egg
        assert recipe.ingredients[1].amount == 2.0
        assert recipe.ingredients[1].unit == unit_piece

    def test_create_ingredient_model_returns_valid_instance(self):
        """IngredientModel.create — возвращает корректный экземпляр"""
        unit_g = MeasurementUnitModel.create("грамм")
        group = ProductGroupModel.create("Продукты")
        flour = ProductModel.create("Мука", "Пшеничная мука", unit_g, group)

        ingredient = IngredientModel.create(flour, 200.0, unit_g)

        assert ingredient.product == flour
        assert ingredient.amount == 200.0
        assert ingredient.unit == unit_g

    def test_product_setter_getter_sets_and_returns_product_model(self):
        """Сеттер/геттер product — корректно сохраняет и возвращает ProductModel"""
        unit_piece = MeasurementUnitModel.create("шт")
        group = ProductGroupModel.create("Продукты")
        egg = ProductModel.create("Яйцо", "Куриное яйцо", unit_piece, group)

        ingredient = IngredientModel()
        ingredient.product = egg

        assert ingredient.product == egg

    def test_amount_setter_getter_sets_and_returns_positive_float(self):
        """Сеттер/геттер amount — корректно сохраняет и возвращает положительное число"""
        unit_g = MeasurementUnitModel.create("грамм")
        ingredient = IngredientModel()
        ingredient.amount = 3.5

        assert ingredient.amount == 3.5

    def test_amount_setter_raises_runtime_error_on_invalid_value(self):
        """Сеттер amount — выбрасывает RuntimeError при значении <= 0"""
        unit_g = MeasurementUnitModel.create("грамм")
        group = ProductGroupModel.create("Продукты")
        flour = ProductModel.create("Мука", "Пшеничная мука", unit_g, group)
        ingredient = IngredientModel()
        ingredient.product = flour
        ingredient.unit = unit_g

        with pytest.raises(RuntimeError):
            ingredient.amount = -1.0

        with pytest.raises(RuntimeError):
            ingredient.amount = 0.0

    def test_product_setter_raises_runtime_error_on_invalid_type(self):
        """Сеттер product — выбрасывает RuntimeError при неверном типе"""
        ingredient = IngredientModel()
        with pytest.raises(RuntimeError):
            ingredient.product = "not_a_product"

    def test_unit_setter_raises_runtime_error_on_invalid_type(self):
        """Сеттер unit — выбрасывает RuntimeError при неверном типе"""
        ingredient = IngredientModel()
        with pytest.raises(RuntimeError):
            ingredient.unit = "not_a_unit"

    # Проверить фабричный метод создания модели из dto
    def test_create_model_from_dto_measurementunit(self):
        # Подготовка
        g_d = {
            "id": "adb7510f-687d-428f-a697-26e53d3f65b7",
            "name": "Грамм",
            "conversion_factor": 1.0
        }
        kg_d = {
            "id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
            "name": "Килограмм",
            "base_unit": {
                "id": "adb7510f-687d-428f-a697-26e53d3f65b7"
            },
            "conversion_factor": 1000.0
        }
        g_dto = create_dto(MeasurementUnitDto, g_d)
        kg_dto: MeasurementUnitDto = create_dto(MeasurementUnitDto, kg_d)

        # Действие
        g = MeasurementUnitModel.from_dto(g_dto, {})
        kg = MeasurementUnitModel.from_dto(kg_dto, {"adb7510f-687d-428f-a697-26e53d3f65b7": g})

        # Проверка
        assert kg.id == "a33dd457-36a8-4de6-b5f1-40afa6193346"
        assert kg.name == "Килограмм"
        assert kg.conversion_factor == 1000.0
        assert kg.base_unit == g

    def test_create_model_from_dto_measurementunit_missing_id_key(self):
        """
        Проверяет, что выбрасывается KeyError, если в словаре,
        который должен ссылаться на объект, отсутствует 'id'.
        """

        # Подготовка
        g_d = {
            "id": "adb7510f-687d-428f-a697-26e53d3f65b7",
            "name": "Грамм",
            "conversion_factor": 1.0
        }
        kg_d = {
            "id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
            "name": "Килограмм",
            "base_unit": {
                "id": "adb7510f-687d-428f-a697-26e53d3f65b7"
            },
            "conversion_factor": 1000.0
        }
        g_dto = create_dto(MeasurementUnitDto, g_d)
        kg_dto: MeasurementUnitDto = create_dto(MeasurementUnitDto, kg_d)

        # Проверка
        with pytest.raises(KeyError) as e:
            g = MeasurementUnitModel.from_dto(g_dto, {})
            kg = MeasurementUnitModel.from_dto(kg_dto, {"113": g})


if __name__ == "__main__":
    pytest.main(['-v'])