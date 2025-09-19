###############################################
# Модель организации
class CompanyModel:
    __name: str = ""
    __inn: str = ""
    __account: str = ""
    __corr_account: str = ""
    __bik: str = ""
    __ownership: str = ""

    def __init__(self, name="", inn="", account="", corr_account="", bik="", ownership=""):
        self.__name = name
        self.__inn = inn
        self.__account = account
        self.__corr_account = corr_account
        self.__bik = bik
        self.__ownership = ownership

    # --- Наименование ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    # --- ИНН ---
    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        self.__inn = value

    # --- Счет ---
    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        self.__account = value

    # --- Корреспондентский счет ---
    @property
    def corr_account(self) -> str:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        self.__corr_account = value

    # --- БИК ---
    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        self.__bik = value

    # --- Вид собственности ---
    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        self.__ownership = value

