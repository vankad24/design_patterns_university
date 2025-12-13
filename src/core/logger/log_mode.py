from enum import IntFlag

class LogMode(IntFlag):
    """
    Режимы вывода логов (можно комбинировать, например: LogMode.CONSOLE | LogMode.FILE )
    """
    CONSOLE = 1   # Вывод в консоль
    FILE = 2      # Запись в файл

