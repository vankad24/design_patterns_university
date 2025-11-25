from src.core.singletone import Singleton
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


