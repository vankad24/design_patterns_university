import os.path
from dataclasses import asdict

from src.core.functions import load_json
from src.core.singletone import Singleton
from src.dto.functions import create_dto
from src.dto.settings_dto import SettingsDto
from src.models.company import CompanyModel
from src.models.settings import SettingsModel
from src.repository import Repository
from src.settings_manager import SettingsManager


####################################################
# Менеджер экспорта данных приложения
class ExportManager(metaclass=Singleton):

    # Экспортировать все данные (settings и repository) в словарь
    @staticmethod
    def export_to_dict()->dict:
        dicts = [
            SettingsManager().dump(),
            Repository().dump()
        ]
        dumped_dict = {}
        for d in dicts:
            dumped_dict.update(d)
        return dumped_dict


