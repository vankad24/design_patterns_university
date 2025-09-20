import json
import os.path

from src.models.company import CompanyModel
from src.utils.singletone import Singleton
from src.models.utils import model_converter, model_validators

####################################################
# Менеджер настроек.
# Предназначен для управления настройками и хранения параметров приложения
class SettingsManager(metaclass=Singleton):
    __file_name: str = ""
    __company: CompanyModel = None

    def __init__(self):
        self.set_default()

    # Параметры организации из настроек
    @property
    def company(self) -> CompanyModel:
        return self.__company

    @property
    def file_name(self) -> str:
        return self.__file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        path = os.path.abspath(value.strip())
        if path == "":
            return

        if os.path.exists(path):
            self.__file_name = path
        else:
            raise Exception(f"Не найден файл настроек: {path}")

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")
        try:
            with open(self.__file_name.strip(), 'r', encoding='utf-8') as file:
                data = json.load(file)

                if "company" in data:
                    model_converter.dict_to_company(data["company"], self.__company)
                    model_validators.validate_company(self.__company)

                    return True
                return False
        except Exception as e:
            return False

    # Параметры настроек по умолчанию
    def set_default(self):
        c = CompanyModel()
        c.name="Копыта и рога"
        c.inn="123456789012"
        c.account="12345678901"
        c.corr_account="10987654321"
        c.bik="123456789"
        c.ownership="00001"
        self.__company = c