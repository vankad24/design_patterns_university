from dataclasses import dataclass
from abc import abstractmethod

import uuid

@dataclass
class AbstractDto:
    id: str = str(uuid.uuid4())