import pytest

from src.dto.functions import create_dto
from src.dto.measurement_dto import MeasurementUnitDto
from src.models.measurement_unit import MeasurementUnitModel


# Проверить фабричный метод и загрузку данных в dto
def test_create_dto_measurementunitdto_with_base_unit():
    # Подготовка
    kg_d = {
        "id": "a33dd457-36a8-4de6-b5f1-40afa6193346",
        "name": "Килограмм",
        "base_unit": {
            "id": "adb7510f-687d-428f-a697-26e53d3f65b7"
        },
        "conversion_factor": 1000.0
    }


    # Действие
    kg_dto: MeasurementUnitDto = create_dto(MeasurementUnitDto, kg_d)

    # Проверка
    assert kg_dto is not None
    assert kg_dto.id == "a33dd457-36a8-4de6-b5f1-40afa6193346"
    assert kg_dto.name == "Килограмм"
    assert kg_dto.conversion_factor == 1000.0
    assert kg_dto.base_unit.id == "adb7510f-687d-428f-a697-26e53d3f65b7"


# Проверить фабричный метод и загрузку данных в dto
def test_create_dto_measurementunitdto_without_base_unit():
    # Подготовка
    g_d = {
        "id": "adb7510f-687d-428f-a697-26e53d3f65b7",
        "name": "Грамм",
        "conversion_factor": 1.0
    }

    # Действие
    g_dto = create_dto(MeasurementUnitDto, g_d)

    # Проверка
    assert g_dto is not None
    assert g_dto.id == "adb7510f-687d-428f-a697-26e53d3f65b7"
    assert g_dto.name == "Грамм"
    assert g_dto.conversion_factor == 1.0
    assert g_dto.base_unit is None



if __name__ == "__main__":
    pytest.main(['-v'])