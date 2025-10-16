from types import GenericAlias

from src.core.functions import get_type_hints_without_underscore
from src.models.abstract_model import AbstractModel
from src.models.recipe import RecipeModel
from src.models.validators.functions import validate_val


def load_from_dict(obj: AbstractModel, data: dict, created_models=None):
    """
    Загружает значения из словаря `data` в объект `obj` на основе type hints.
    Если поле является потомком AbstractModel, подставляет объект из created_models.
    При этом предоставляет информативные ошибки при KeyError.

    :param obj: объект AbstractModel, в который загружаются данные
    :param data: словарь с данными
    :param created_models: словарь уже созданных моделей по id
    :return: обновлённый словарь created_models
    """
    if created_models is None:
        created_models = {}
    validate_val(data, dict)
    validate_val(created_models, dict)

    hint_types = get_type_hints_without_underscore(obj.__class__)

    for key, value in data.items():
        if not key.startswith("_") and hasattr(obj, key):
            attr_type = hint_types.get(key, None)

            try:
                # Список моделей
                if attr_type and isinstance(attr_type, GenericAlias) and \
                        issubclass(attr_type.__origin__, list) and \
                        issubclass(attr_type.__args__[0], AbstractModel):
                    arr = []
                    for item in value:
                        if 'id' not in item:
                            raise KeyError(f"Отсутствует 'id' в словаре элемента списка для ключа '{key}': {item}")
                        if item['id'] not in created_models:
                            raise KeyError(f"Не найден объект с id='{item['id']}' для ключа '{key}': {item}")
                        arr.append(created_models[item['id']])
                    setattr(obj, key, arr)

                # Отдельная модель
                elif attr_type and isinstance(attr_type, type) and \
                        issubclass(attr_type, AbstractModel) and isinstance(value, dict):
                    if 'id' not in value:
                        raise KeyError(f"Отсутствует 'id' в словаре для ключа '{key}': {value}")
                    if value['id'] not in created_models:
                        raise KeyError(f"Не найден объект с id='{value['id']}' для ключа '{key}': {value}")
                    model_obj = created_models[value['id']]
                    setattr(obj, key, model_obj)

                # Простое поле
                else:
                    setattr(obj, key, value)

            except KeyError as e:
                raise KeyError(f"Ошибка при загрузке ключа '{key}' со значением '{value}': {e}") from e

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

    md_lines.append("---\n")  # разделитель в конце
    return "\n".join(md_lines)
