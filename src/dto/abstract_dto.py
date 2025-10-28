from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class AbstractDto:
    id: str = ""
    name: str = ""