import json
import os.path

from src.models.company import CompanyModel
from src.utils.singletone import Singleton


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

    # Конвертация словаря в объект CompanyModel
    def convert(self, data: dict, to_company_obj=None) -> CompanyModel:
        if to_company_obj is None:
            company = CompanyModel()
        else:
            company = to_company_obj
        if "name" in data:
            company.name = data["name"]
        if "inn" in data:
            company.inn = data["inn"]
        if "account" in data:
            company.account = data["account"]
        if "corr_account" in data:
            company.corr_account = data["corr_account"]
        if "bik" in data:
            company.bik = data["bik"]
        if "ownership" in data:
            company.ownership = data["ownership"]
        return company

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")
        try:
            with open(self.__file_name.strip(), 'r', encoding='utf-8') as file:
                data = json.load(file)

                if "company" in data:
                    self.__company = self.convert(data["company"], self.__company)
                    return True
                return False
        except Exception as e:
            return False

    # Параметры настроек по умолчанию
    def set_default(self):
        self.__company = CompanyModel()
        self.__company.name = "Копыта и рога"