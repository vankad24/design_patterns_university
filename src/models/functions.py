from src.models.recipe import RecipeModel


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
