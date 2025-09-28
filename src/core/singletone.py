class Singleton(type):
    """
    Метакласс для реализации паттерна Singleton.
    Гарантирует, что у класса будет только один экземпляр.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Создаёт новый экземпляр класса только если он ещё не был создан.
        В противном случае возвращает уже существующий экземпляр.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
