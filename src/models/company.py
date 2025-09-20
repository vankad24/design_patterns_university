from src.models.utils.validators import validate_str

###############################################
# Модель организации
class CompanyModel:
    __name: str = ""
    __inn: str = ""
    __account: str = ""
    __corr_account: str = ""
    __bik: str = ""
    __ownership: str = ""

    # --- Наименование ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Наименование не может быть пустым")
        self.__name = value.strip()

    # --- ИНН ---
    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        self.__inn = validate_str(value, 12, "ИНН", True)

    # --- Счет ---
    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        self.__account = validate_str(value, 11, "Счет", True)

    # --- Корреспондентский счет ---
    @property
    def corr_account(self) -> str:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        self.__corr_account = validate_str(value, 11, "Корреспондентский счет", True)

    # --- БИК ---
    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        self.__bik = validate_str(value, 9, "БИК", True)

    # --- Вид собственности ---
    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        self.__ownership = validate_str(value, 5, "Вид собственности")