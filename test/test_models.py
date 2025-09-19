import os.path

from src.models.utils import model_converter
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


if __name__ == "__main__":
    pytest.main(['-v'])