import pytest
from src.repository import RepoKeys
from src.start_service import StartService

class TestStartService:
    StartService().start()

    @pytest.fixture
    def service(self):
        return StartService()

    def test_units_created(self, service):
        """Проверяет, что все стандартные единицы измерения созданы корректно
        и имеют правильные связи (base_unit для кг)."""
        units = service.repo.data[RepoKeys.MEASUREMENT_UNITS]
        grams = units['adb7510f-687d-428f-a697-26e53d3f65b7']
        kg = units['a33dd457-36a8-4de6-b5f1-40afa6193346']
        piece = units['f8346e8b-7260-4db8-a673-c8c826ab08b7']
        ml = units['4f39246a-2e29-4d15-9a09-1f86b72f6ce0']

        assert grams.name == "Грамм"
        assert kg.base_unit == grams
        assert piece.name == "Штуки"
        assert ml.name == "Миллилитр"

    def test_product_groups_created(self, service):
        """Проверяет создание всех стандартных групп продуктов и их имена."""
        groups = service.repo.data[RepoKeys.PRODUCT_GROUPS]
        food = groups['7f4ecdab-0f01-4216-8b72-4c91d22b8918']
        spices = groups['3b6f4ac1-5dbb-4d35-9a1f-6d3db9f41077']
        dairy = groups['b8d9c3f2-fc57-4c6f-8b70-3f6baf2b8d61']

        assert food.name == "Продукты питания"
        assert spices.name == "Специи"
        assert dairy.name == "Молочные продукты"

    def test_products_created(self, service):
        """Проверяет, что все стандартные продукты созданы,
        принадлежат правильным группам и используют корректные единицы измерения."""
        products = service.repo.data[RepoKeys.PRODUCTS]
        units = service.repo.data[RepoKeys.MEASUREMENT_UNITS]
        groups = service.repo.data[RepoKeys.PRODUCT_GROUPS]

        flour = products['0c101a7e-5934-4155-83a6-d2c388fcc11a']
        sugar = products['5d7a3b4e-9851-4ac7-9f82-0937d9cb7d77']
        egg = products['e0f1a8f3-812d-4f9b-bde8-9b0f6b178a2e']
        mozzarella = products['d3a84b11-5f38-4c73-a217-b57b05dba2b0']

        assert flour.unit == units['adb7510f-687d-428f-a697-26e53d3f65b7']
        assert flour.group == groups['7f4ecdab-0f01-4216-8b72-4c91d22b8918']
        assert sugar.unit == units['adb7510f-687d-428f-a697-26e53d3f65b7']
        assert egg.unit == units['f8346e8b-7260-4db8-a673-c8c826ab08b7']
        assert mozzarella.unit == units['adb7510f-687d-428f-a697-26e53d3f65b7']

    def test_ingredients_belong_to_products_and_units(self, service):
        """Проверяет, что все ингредиенты ссылаются на существующие продукты
        и используют существующие единицы измерения."""
        ingredients = service.repo.data[RepoKeys.INGREDIENTS]
        products = service.repo.data[RepoKeys.PRODUCTS]
        units = service.repo.data[RepoKeys.MEASUREMENT_UNITS]

        for ing in ingredients.values():
            assert ing.product in products.values()
            assert ing.unit in units.values()

    def test_recipes_created_with_ingredients(self, service):
        """Проверяет, что все стандартные рецепты созданы и содержат ингредиенты,
        которые существуют в репозитории."""
        recipes = service.repo.data[RepoKeys.RECIPES]
        ingredients = service.repo.data[RepoKeys.INGREDIENTS]

        waffles = recipes['de0e0123-0442-4d14-bbf9-053eefbfe907']
        pizza = recipes['5bfa1e24-6f59-46a0-91d4-7b987b5fd31e']

        for recipe in [waffles, pizza]:
            assert len(recipe.ingredients) > 0
            for ing_ref in recipe.ingredients:
                assert ing_ref in ingredients.values()


if __name__ == "__main__":
    pytest.main(['-v'])