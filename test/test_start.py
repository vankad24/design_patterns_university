import pytest

from src.start_service import StartService

class TestStartService:
    def test_start_service_creates_all_entities(self):
        """
        Проверяет, что метод start создаёт все стандартные единицы измерения,
        группы, продукты и рецепты.
        """
        service = StartService()
        service.start()

        # --- Единицы измерения ---
        # todo service.__measurement_units ???
        units = {u.name: u for u in service.repo.measurement_units}
        grams = units.get("грамм")
        kg = units.get("кг")
        piece = units.get("шт")
        ml = units.get("мл")

        assert grams is not None
        assert kg is not None and kg.base_unit == grams
        assert piece is not None
        assert ml is not None

        # --- Группы ---
        groups = {g.name: g for g in service.repo.product_groups}
        food = groups.get("Продукты питания")
        spices = groups.get("Специи")
        dairy = groups.get("Молочные продукты")
        assert food is not None
        assert spices is not None
        assert dairy is not None

        # --- Продукты ---
        products = {p.name: p for p in service.repo.products}
        flour = products.get("Пшеничная мука")
        sugar = products.get("Сахар")
        egg = products.get("Яйцо")
        mozzarella = products.get("Моцарелла")

        assert flour is not None and flour.unit == grams and flour.group == food
        assert sugar is not None and sugar.unit == grams
        assert egg is not None and egg.unit == piece
        assert mozzarella is not None

        # --- Рецепты ---
        recipes = {r.name: r for r in service.repo.recipes}
        waffles = recipes.get("Вафли")
        pizza = recipes.get("Пицца")
        assert waffles is not None and len(waffles.ingredients) > 0
        assert pizza is not None and len(pizza.ingredients) > 0

    def test_add_unit_and_retrieve(self):
        """
        Проверяет корректность метода add_unit и хранение в репозитории.
        """
        service = StartService()
        gram = service.add_unit("грамм")
        units = {u.name: u for u in service.repo.measurement_units}
        assert units["грамм"] == gram

    def test_add_product_group_and_product(self):
        """
        Проверяет методы add_product_group и add_product.
        """
        service = StartService()
        food_group = service.add_product_group("Продукты питания")
        groups = {g.name: g for g in service.repo.product_groups}
        assert groups["Продукты питания"] == food_group

        gram = service.add_unit("грамм")
        flour = service.add_product("Мука", "Пшеничная мука", gram, food_group)
        products = {p.name: p for p in service.repo.products}
        assert products["Мука"] == flour

    def test_add_recipe(self):
        """
        Проверяет метод add_recipe.
        """
        service = StartService()
        food_group = service.add_product_group("Продукты")
        gram = service.add_unit("грамм")
        flour = service.add_product("Мука", "Пшеничная мука", gram, food_group)
        sugar = service.add_product("Сахар", "Сахар белый", gram, food_group)

        recipe = service.add_recipe("Тесто", [(flour, 100.0), (sugar, 50.0)], "Инструкция")
        recipes = {r.name: r for r in service.repo.recipes}
        assert recipes["Тесто"] == recipe
        assert len(recipe.ingredients) == 2


if __name__ == "__main__":
    pytest.main(['-v'])