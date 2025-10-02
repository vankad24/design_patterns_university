from src.core.singletone import Singleton


class Repository(metaclass=Singleton):
    MEASUREMENT_UNIT_KEY = "measurement_unit_model"

    __data = {}

    @property
    def data(self):
        return self.__data

