from src.models.abstract_model import AbstractModel
from src.models.validators.decorators import validate_setter
from src.models.validators.functions import not_empty


###############################################
# Модель организации
class CompanyModel(AbstractModel):
    def __init__(self):
        super().__init__()

    # Наименование организации
    _name: str = ""
    # Идентификационный номер налогоплательщика (ИНН)
    _inn: str = ""
    # Расчетный счет организации
    _account: str = ""
    # Корреспондентский счет банка организации
    _corr_account: str = ""
    # Банк идентификационный код (БИК)
    _bik: str = ""
    # Вид собственности организации
    _ownership: str = ""

    # --- Наименование ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @validate_setter(str, check_func=not_empty)
    def name(self, value: str):
        self._name = value.strip()

    # --- ИНН ---
    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    @validate_setter(str, 12, check_func=str.isdigit)
    def inn(self, value: str):
        self._inn = value

    # --- Счет ---
    @property
    def account(self) -> str:
        return self._account

    @account.setter
    @validate_setter(str, 11, check_func=str.isdigit)
    def account(self, value: str):
        self._account = value

    # --- Корреспондентский счет ---
    @property
    def corr_account(self) -> str:
        return self._corr_account

    @corr_account.setter
    @validate_setter(str, 11, check_func=str.isdigit)
    def corr_account(self, value: str):
        self._corr_account = value

    # --- БИК ---
    @property
    def bik(self) -> str:
        return self._bik

    @bik.setter
    @validate_setter(str, 9, check_func=str.isdigit)
    def bik(self, value: str):
        self._bik = value

    # --- Вид собственности ---
    @property
    def ownership(self) -> str:
        return self._ownership

    @ownership.setter
    @validate_setter(str, 5)
    def ownership(self, value: str):
        self._ownership = value