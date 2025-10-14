from types import GenericAlias

from src.core.functions import get_type_hints_without_underscore
from src.models.abstract_model import AbstractModel
from src.models.recipe import RecipeModel
from src.models.validators.functions import validate_val


def load_from_dict(obj: AbstractModel, data: dict, created_models=None):
    """
    Загружает данные из словаря в атрибуты объекта.
    Игнорирует ключи, начинающиеся с '_', и отсутствующие атрибуты.
    """
    if created_models is None:
        created_models = {}
    validate_val(data, dict)
    validate_val(created_models, dict)
    hint_types = get_type_hints_without_underscore(obj.__class__)
    for key, value in data.items():
        if not key.startswith("_") and hasattr(obj, key):
            # класс поля взятый из type hint
            attr_type = hint_types.get(key, None)
            # если поле является потомком AbstractModel и при этом в него загружается словарь
            if attr_type and isinstance(attr_type, GenericAlias) and issubclass(attr_type.__origin__, list) and issubclass(attr_type.__args__[0], AbstractModel):
                arr = []
                for item in value:
                    arr.append(created_models[item['id']])
                setattr(obj, key, arr)
            elif attr_type and isinstance(attr_type, type) and issubclass(attr_type, AbstractModel) and isinstance(value, dict):
                # в этом словаре обязательно должен быть id, который должен присутствовать в созданных объектах
                model_obj = created_models[value['id']]
                setattr(obj, key, model_obj)
                # todo exceptions
            else:
                setattr(obj, key, value)
    return created_models


def recipe_to_markdown(recipe: RecipeModel) -> str:
    """
    Генерирует markdown строку из RecipeModel
    """
    md_lines = list()

    # Название рецепта
    md_lines.append(f"## {recipe.name}\n")

    # Время приготовления
    if recipe.cooking_time:
        md_lines.append(f"**Время приготовления:** {recipe.cooking_time}\n")

    # Ингредиенты
    if recipe.ingredients:
        md_lines.append("**Ингредиенты:**\n")
        for ing in recipe.ingredients:
            product_name = ing.product.name if ing.product else "Неизвестный продукт"
            amount = ing.amount
            unit_name = ing.unit.name if ing.unit else ""
            md_lines.append(f"* {product_name} – {amount} {unit_name}".strip())
        md_lines.append("")  # пустая строка после списка

    # Пошаговая инструкция
    if recipe.steps:
        md_lines.append("**Инструкция:**\n")
        for i, step in enumerate(recipe.steps, start=1):
            md_lines.append(f"{i}. {step}")
        md_lines.append("")  # пустая строка после инструкции

    md_lines.append("---")  # разделитель в конце
    return "\n".join(md_lines)
