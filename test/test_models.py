import os.path

from src.models.utils import model_converter, model_validators
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
    def test_load_model_company_model(self):
        # Подготовка
        file_name = '../settings.json'
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True
        assert manager.company.name == 'Рога и копыта'

    # Проверить создание основной модели
    # Данные загружаем через json настройки c абослютным путём
    def test_load_model_company_model_abs(self):
        # Подготовка
        file_name = os.path.abspath('../settings.json')

        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True
        assert manager.company.name == 'Рога и копыта'

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
        assert manager.company == manager2.company

    # Проверка создания CompanyModel из словаря
    def test_convert_creates_company_from_dict(self):
        # Подготовка
        data = {
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001"
        }

        # Действие
        company = model_converter.dict_to_company(data)

        # Проверки
        assert company.name == data["name"]
        assert company.inn == data["inn"]
        assert company.account == data["account"]
        assert company.corr_account == data["corr_account"]
        assert company.bik == data["bik"]
        assert company.ownership == data["ownership"]

    # Проверка создания CompanyModel при загрузке из json файла
    def test_convert_creates_company_from_dir(self):
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
        company = manager.company

        # Проверки
        assert company.name == data["name"]
        assert company.inn == data["inn"]
        assert company.account == data["account"]
        assert company.corr_account == data["corr_account"]
        assert company.bik == data["bik"]
        assert company.ownership == data["ownership"]

    # Проверка обработки ошибок при некорректной конвертации CompanyModel
    # при неправильном параметре data:dict
    def test_exception_convert_dict_to_company_wrong_dict(self):
        with pytest.raises(ValueError) as exc_info:
            model_converter.dict_to_company(None)
        assert exc_info.value.args[0] == "Для конвертации нужен словарь"

        with pytest.raises(ValueError) as exc_info:
            model_converter.dict_to_company(["name"])
        assert exc_info.value.args[0] == "Для конвертации нужен словарь"

    # Проверка обработки ошибок при некорректной конвертации CompanyModel
    # при отсутствии обязательных ключей в словаре
    @pytest.mark.parametrize("missing_key", ["name", "inn", "account", "corr_account", "bik", "ownership"])
    def test_exception_convert_dict_to_company_missing_key(self, missing_key):
        data = {
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001"
        }
        data.pop(missing_key)

        with pytest.raises(ValueError) as exc_info:
            model_converter.dict_to_company(data)
        assert exc_info.value.args[0] == f"В словаре нет обязательного значения '{missing_key}'"

    @pytest.mark.parametrize(
        "field, value, error_msg",
        [
            ("name", "   ", "Наименование не может быть пустым"),
            ("inn", "123", "ИНН должен содержать ровно 12 символов"),
            ("inn", "123456789012435", "ИНН должен содержать ровно 12 символов"),
            ("inn", "12345678901a", "ИНН должен содержать только цифры"),
            ("account", "123", "Счет должен содержать ровно 11 символов"),
            ("account", "1234567890a", "Счет должен содержать только цифры"),
            ("corr_account", "123", "Корреспондентский счет должен содержать ровно 11 символов"),
            ("corr_account", "1234567890a", "Корреспондентский счет должен содержать только цифры"),
            ("bik", "123", "БИК должен содержать ровно 9 символов"),
            ("bik", "12345678a", "БИК должен содержать только цифры"),
            ("ownership", "1234", "Вид собственности должен содержать ровно 5 символов"),
            ("ownership", "abda", "Вид собственности должен содержать ровно 5 символов"),
            ("ownership", "1234a234ds", "Вид собственности должен содержать ровно 5 символов"),
        ]
    )
    def test_validate_company_fields(self, field, value, error_msg):
        data = {
            "name": "ООО Ромашка",
            "inn": "123456789012",
            "account": "12345678901",
            "corr_account": "10987654321",
            "bik": "123456789",
            "ownership": "00001"
        }

        data[field] = value
        company = model_converter.dict_to_company(data)

        with pytest.raises(ValueError) as exc_info:
            model_validators.validate_company(company)
        assert exc_info.value.args[0] == error_msg


if __name__ == "__main__":
    pytest.main(['-v'])