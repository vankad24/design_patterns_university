from datetime import datetime
from pathlib import Path

from src.core.logger.log_level import LogLevel
from src.core.logger.log_mode import LogMode
from src.core.singletone import Singleton
from src.dto.logger_dto import LoggerDto
from src.models.validators.decorators import validate_setter
from src.models.validators.exceptions import OperationException


class MyLogger(metaclass=Singleton):
    _log_dir = Path("logs")
    _mode = LogMode.CONSOLE
    _log_level = LogLevel.INFO
    _msg_format = "{level}:     {time} - \"{msg}\"\n"
    _filename_format = "log%Y-%m-%d.log"

    @property
    def log_dir(self) -> Path:
        return self._log_dir

    @log_dir.setter
    @validate_setter((str, Path))
    def log_dir(self, value: str | Path):
        self._log_dir = Path(value)

    @property
    def mode(self) -> LogMode:
        return self._mode

    @mode.setter
    @validate_setter((int, LogMode))
    def mode(self, value: int | LogMode):
        self._mode = LogMode(value)

    @property
    def log_level(self) -> LogLevel:
        return self._log_level

    @log_level.setter
    @validate_setter((int, LogLevel))
    def log_level(self, value: int | LogLevel):
        self._log_level = LogLevel(value)

    @property
    def msg_format(self) -> str:
        return self._msg_format

    @msg_format.setter
    @validate_setter(str)
    def msg_format(self, value: str):
        self._msg_format = value

    @property
    def filename_format(self) -> str:
        return self._filename_format

    @filename_format.setter
    @validate_setter(str)
    def filename_format(self, value: str):
        self._filename_format = value

    def log(self, level: LogLevel, msg: str):
        if level < self.log_level:
            # Если уровень логирования недостаточный - выходим
            return
        now = datetime.now()
        log_msg = self.msg_format.format(time=now,level=level.name,msg=msg.strip())
        for mode in self.mode:
            match mode:
                case LogMode.CONSOLE:
                    print(log_msg, end="")
                case LogMode.FILE:
                    self.log_dir.mkdir(parents=True, exist_ok=True)
                    path = self.log_dir / now.strftime(self.filename_format)
                    try:
                        with open(path, mode="a", encoding="utf-8") as file:
                            file.write(log_msg)
                    except Exception as e:
                        raise OperationException(f"Ошибка логирования в файл `{path}`: {e.__class__.__name__} {e}. Сообщение лога: {log_msg}")

    @staticmethod
    def from_dto(dto: LoggerDto, cache: dict):
        """
            Фабричный метод для загрузки настроек в MyLogger из dto
        """
        l = MyLogger()
        l.log_dir = dto.log_dir
        l.mode = dto.mode
        l.log_level = dto.log_level
        l.msg_format = dto.msg_format
        l.filename_format = dto.filename_format
        return l

    def to_dto(self):
        """
            Перевести логгер в DTO
        """
        return LoggerDto(
            log_dir=str(self.log_dir),
            mode=int(self.mode),
            log_level=int(self.log_level),
            msg_format=self.msg_format,
            filename_format=self.filename_format,
        )


