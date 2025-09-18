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
    # Данные загружаем. Проверяем работу Singletone
    def test_load_model_company_model_from_same_file(self):
        # Подготовка
        file_name = '../settings.json'
        manager = SettingsManager()
        manager.file_name = file_name
        initialized_company = manager.company
        manager2 = SettingsManager()

        # Действие
        manager.load()
        manager2.load()

        # Проверки
        assert manager.company == manager2.company
        assert initialized_company == manager.company


if __name__ == "__main__":
    pytest.main(['-v'])