from dataclasses import dataclass, field
from src.core.singletone import Singleton


@dataclass
class Repository(metaclass=Singleton):
    measurement_units: list = field(default_factory=list)
    products: list = field(default_factory=list)
    product_groups: list = field(default_factory=list)
    recipes: list = field(default_factory=list)
