import json
import os.path

from src.models.company import CompanyModel

####################################################3
# Менеджер настроек.
# Предназначен для управления настройками и хранения параметров приложения
class SettingsManager:
    __file_name: str = ""
    __company: CompanyModel = None
    _instance = None

    # Singletone
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
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
        path = value.strip()
        if path == "":
            return

        if os.path.exists(path):
            self.__file_name = path
        else:
            raise Exception("Не найден файл настроек!")

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")
        try:
            with open(self.__file_name.strip(), 'r', encoding='utf-8') as file:
                data = json.load(file)

                if "company" in data.keys():
                    item = data["company"]

                    self.__company.name = item["name"]
                    return True
                return False
        except Exception as e:
            return False

    # Параметры настроек по умолчанию
    def set_default(self):
        self.__company = CompanyModel()
        self.__company.name = "Копыта и рога"