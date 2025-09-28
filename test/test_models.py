import os.path
import uuid

from src.models.measurement_unit import MeasurementUnitModel
from src.models.product import ProductModel
from src.models.product_group import ProductGroupModel
from src.models.storage import StorageModel
from src.models.validators.exceptions import ArgumentException
from src.settings_manager import SettingsManager
from src.models.company import CompanyModel

import pytest

class TestModels:

    # Проверка создания основной модели
    # Данные после создания должны быть пустыми
    def test_create_model_empty_company_model(self):
        # Подготовка
        model = CompanyModel()
        # Действие

        # Проверки
        assert model.name == ""

    # Проверка создания основной модели
    # Данные после создания не должны быть пустыми
    def test_create_model_not_empty_company_model(self):
        # Подготовка
        model = CompanyModel()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_company_model(self):
        # Подготовка
        file_name = '../settings.json'
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True
        assert manager.settings.company.name == 'Рога и копыта'

    # Проверить создание основной модели
    # Данные загружаем через json настройки c абослютным путём
    def test_load_company_model_abs_path(self):
        # Подготовка
        file_name = os.path.abspath('../settings.json')

        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True
        assert manager.settings.company.name == 'Рога и копыта'

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_load_model_company_model_from_same_file(self):
        # Подготовка
        file_name = '../settings.json'
        manager = SettingsManager()
        manager.file_name = file_name
        manager2 = SettingsManager()

        # Действие
        manager.load()
        manager2.load()

        # Проверки
        assert manager.settings.company == manager2.settings.company

    # Проверка загрузки данных в CompanyModel из словаря
    def test_load_from_dict_company(self):
        # Подготовка
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

    # Проверка создания CompanyModel при загрузке из json файла
    def test_load_from_dict_company_from_dir(self):
        # Подготовка
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

    # Проверка обработки ошибок при некорректной конвертации CompanyModel
    # при неправильном параметре data:dict
    def test_load_from_dict_exception_wrong_arg(self):
        company = CompanyModel()
        with pytest.raises(ArgumentException) as exc_info:
            company.load_from_dict(None)
        assert exc_info.value.args[0] == "Пустой аргумент"

        with pytest.raises(ArgumentException) as exc_info:
            company.load_from_dict(["name"])
        assert exc_info.value.args[0].startswith("Некорректный тип")

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
        # Подготовка
        myid = uuid.uuid4().hex
        storage1 = StorageModel()
        storage2 = StorageModel()
        storage1.id = myid
        storage2.id = myid

        # Действие

        # Проверки
        assert storage1 == storage2

    def test_not_equals_storage_models_creation(self):
        # Подготовка
        storage1 = StorageModel()
        storage2 = StorageModel()
        # Действие

        # Проверки
        assert storage1 != storage2

    def test_storage_model_creation(self):
        storage = StorageModel()
        storage.name = "Основной склад"
        storage.address = "г. Москва, ул. Ленина, 1"

        assert storage.name == "Основной склад"
        assert storage.address == "г. Москва, ул. Ленина, 1"


    def test_measurement_unit_creation(self):
        # Подготовка
        gram = MeasurementUnitModel("грамм", 1.0)
        kg = MeasurementUnitModel("кг", 1000.0, gram)

        # Проверки
        assert gram.base_unit == gram
        assert kg.base_unit == gram

    def test_convert_measurement_unit_chain_conversion(self):
        # Подготовка
        gram = MeasurementUnitModel("грамм", 1.0)  # базовая единица
        kg = MeasurementUnitModel("кг", 1000.0, gram)  # 1 кг = 1000 г
        ton = MeasurementUnitModel("т", 1000.0, kg)  # 1 т = 1000 кг

        # Проверки
        assert ton.convert_to(2, gram) == 2_000_000
        assert kg.convert_to(5, gram) == 5000
        assert ton.convert_to(1, kg) == 1000
        assert kg.convert_to(5, kg) == 5
        assert gram.convert_to(2, gram) == 2


    def test_product_group_and_product_creation(self):
        group = ProductGroupModel()
        group.name = "Молочные продукты"

        long_name = "a"*50
        long_full_name = "a"*255

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
        product = ProductModel()
        long_name = "a" * 51
        long_full_name = "a" * 256

        with pytest.raises(RuntimeError) as exc_info:
            product.name = long_name

        with pytest.raises(RuntimeError) as exc_info:
            product.full_name = long_full_name


if __name__ == "__main__":
    pytest.main(['-v'])