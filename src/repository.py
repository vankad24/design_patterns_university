from dataclasses import dataclass, field
from enum import StrEnum

from src.core.singletone import Singleton

class RepoKeys(StrEnum):
    MEASUREMENT_UNITS = "measurement_units"
    PRODUCT_GROUPS = "product_groups"
    PRODUCTS = "products"
    INGREDIENTS = "ingredients"
    RECIPES = "recipes"


class Repository(metaclass=Singleton):
    __data: dict = None

    def __init__(self):
        self.__data = {}
        for key in RepoKeys:
            self.__data[str(key)] = {}

    @property
    def data(self):
        return self.__data

