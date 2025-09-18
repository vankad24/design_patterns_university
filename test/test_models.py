from src.settings_manager import SettingsManager
from src.models.company import CompanyModel

import pytest
import json

class TestModels:

    # Проверка создания основной модели
    # Данные после создания должны быть пусными
    def test_create_model_empty_company_model(self):
        # Подготовка
        model = CompanyModel()
        # Действие

        # Проверки
        assert model.name == ""

    # Проверка создания основной модели
    # Данные после создания не должны быть пусными
    def test_create_model_not_empty_company_model(self):
        # Подготовка
        model = CompanyModel()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    def test_load_model_company_model(self):
        # Подготовка
        file_name = '../settings.json'
        manager = SettingsManager(file_name)

        # Действие
        result = manager.load()

        # Проверки
        assert result == True

    def test_load_model_company_model_from_same_file(self):
        # Подготовка
        file_name = '../../settings.json'
        manager = SettingsManager(file_name)
        manager2 = SettingsManager(file_name)

        # Действие
        manager.load()
        manager2.load()

        # Проверки
        assert manager.company == manager2.company


if __name__ == "__main__":
    pytest.main(['-v'])