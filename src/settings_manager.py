import json
import os.path

from src.models.company import CompanyModel


class SettingsManager():
    __file_name:str = ""
    __company: CompanyModel = None

    # singletone
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.default()

    @property
    def company(self):
        return self.__company

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if value.strip() == "":
            return
        if os.path.exists(value):
            self.__file_name == value.strip()

    def load(self):
        if self.__file_name.strip() == "":
            raise FileNotFoundError(f"Файл не найден: {self.__file_name} в директории {os.getcwd()}")
        try:
            with open(self.__file_name) as file:
                data = json.load(file)
            if "company" in data:
                item = data["company"]
                self.__company.name = item["name"]
                return True
            return False

        except Exception as e:
            return False

    def default(self):
        self.__company = CompanyModel()
        self.__company.name = "Рога и копыта"




    # def load_settings(self, data, company_model):
    #     item = data['company']
    #     company_model.name = item['name']
    #
    # @classmethod
    # def read_json(cls, file_name, ):
    #     with open(file_name) as file:
    #         return json.load(file)
    #
    # def get_company(self):
    #     company_model = CompanyModel()
    #     self.load_settings(self.data, company_model)
    #     return company_model