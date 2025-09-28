from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter

###############################################
# Модель организации
class CompanyModel(AbstractModel):
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
    @validate_setter(str, check_func=lambda x: len(x.strip())>0)
    def name(self, value: str):
        self.__name = value.strip()

    # --- ИНН ---
    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    @validate_setter(str, 12, check_func=str.isdigit)
    def inn(self, value: str):
        self.__inn = value

    # --- Счет ---
    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    @validate_setter(str, 11, check_func=str.isdigit)
    def account(self, value: str):
        self.__account = value

    # --- Корреспондентский счет ---
    @property
    def corr_account(self) -> str:
        return self.__corr_account

    @corr_account.setter
    @validate_setter(str, 11, check_func=str.isdigit)
    def corr_account(self, value: str):
        self.__corr_account = value

    # --- БИК ---
    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    @validate_setter(str, 9, check_func=str.isdigit)
    def bik(self, value: str):
        self.__bik = value

    # --- Вид собственности ---
    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    @validate_setter(str, 5)
    def ownership(self, value: str):
        self.__ownership = value