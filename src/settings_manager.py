import os.path
from dataclasses import asdict

from src.core.functions import load_json
from src.core.singletone import Singleton
from src.dto.functions import create_dto
from src.dto.settings_dto import SettingsDto
from src.models.company import CompanyModel
from src.models.settings import SettingsModel


####################################################
# Менеджер настроек.
# Предназначен для управления настройками и хранения параметров приложения
class SettingsManager(metaclass=Singleton):
    __file_name: str = "./settings.json"
    __settings: SettingsModel = None

    # ключ для сохранения в конфиг
    CONFIG_KEY = "settings"

    def __init__(self):

        self.set_default()
        self.load()

    @property
    def settings(self) -> SettingsModel:
        return self.__settings

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
            raise FileNotFoundError(f"Не найден файл настроек: {path}")

    # Загрузить настройки из Json файла
    def load(self):
        data = load_json(self.__file_name)[self.CONFIG_KEY]
        self.__settings = SettingsModel.from_dto(create_dto(SettingsDto, data), {})

    # Выгрузить настройки в словарь
    def dump(self) -> dict:
        return {self.CONFIG_KEY: asdict(self.__settings.to_dto())}

    # Параметры настроек по умолчанию
    def set_default(self):
        c = CompanyModel()
        c.name="Копыта и рога"
        c.inn="123456789012"
        c.account="12345678901"
        c.corr_account="10987654321"
        c.bik="123456789"
        c.ownership="00001"

        self.__settings = SettingsModel()
        self.__settings.company = c

