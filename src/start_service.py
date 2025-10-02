from src.core.singletone import Singleton
from src.models.measurement_unit import MeasurementUnitModel
from src.repository import Repository


class StartService:
    __repo: Repository = Repository()

    def __init__(self):
        self.__repo.data[Repository.MEASUREMENT_UNIT_KEY] = []

    @property
    def data(self):
        return self.__repo.data

    def default_create_measurement_unit(self):
        arr = self.__repo.data[Repository.MEASUREMENT_UNIT_KEY]
        kg = MeasurementUnitModel.create_kg()
        arr.append(kg.base_unit)
        arr.append(kg)


    def start(self):
        self.default_create_measurement_unit()