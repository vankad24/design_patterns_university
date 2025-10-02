import pytest

from src.models.measurement_unit import MeasurementUnitModel
from src.repository import Repository
from src.start_service import StartService

start_service = StartService()
start_service.start()

class TestStart:

    def test_start_service_measurement_not_empty(self):
        # Подготовка
        units: list[MeasurementUnitModel] = start_service.data[Repository.MEASUREMENT_UNIT_KEY]
        gramm = units[0]
        kg = units[1]

        # Действие

        # Проверки
        assert len(units) == 2
        assert kg.base_unit == gramm



if __name__ == "__main__":
    pytest.main(['-v'])