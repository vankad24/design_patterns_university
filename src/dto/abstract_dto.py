import uuid
from dataclasses import dataclass


@dataclass
class AbstractDto:
    id: str = str(uuid.uuid4())