###############################################
# Модель организации
class CompanyModel:
    __name: str = ""
    __inn: str = ""
    __account: str = ""
    __corr_account: str = ""
    __bik: str = ""
    __ownership: str = ""

    # --- Вспомогательный метод ---
    def __validate_str(self, value: str, length: int, field: str) -> str:
        value = value.strip()
        if len(value) != length:
            raise ValueError(f"{field} должен содержать ровно {length} символов")
        return value

    # --- Наименование ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Наименование не может быть пустым")
        self.__name = value

    # --- ИНН (12 символов) ---
    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        self.__inn = self.__validate_str(value, 12, "ИНН")

    # --- Счет (11 символов) ---
    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        self.__account = self.__validate_str(value, 11, "Счет")

    # --- Корреспондентский счет (11 символов) ---
    @property
    def corr_account(self) -> str:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        self.__corr_account = self.__validate_str(value, 11, "Корреспондентский счет")

    # --- БИК (9 символов) ---
    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        self.__bik = self.__validate_str(value, 9, "БИК")

    # --- Вид собственности (5 символов) ---
    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        self.__ownership = self.__validate_str(value, 5, "Вид собственности")

