from dataclasses import dataclass

from src.dto.abstract_dto import AbstractDto


# класс dto для логгера
@dataclass
class LoggerDto(AbstractDto):
    log_dir: str = "logs"
    mode: int = 1
    log_level: int = 1
    msg_format: str = "{time} - {level} - \"{msg}\"\n"
    filename_format: str = "log%Y-%m-%d_%H:%M:%S.log"
