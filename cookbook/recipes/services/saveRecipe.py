from cookbook.models import Recipe, RecipeIngredients, RecipeInstructions, Categories

def saveNameAndDesc(recipeForm, user_id):
    # Check recipe name and description
    if not recipeForm.name.data:
        raise Exception("Recipe name can't be empty")
    elif not recipeForm.description.data:
        raise Exception("Recipe description can't be empty")

    # Create recipe object and add to session
    recipe = Recipe(name=recipeForm.name.data, description=recipeForm.description.data, user_id=user_id)
    return recipe

def saveCategories(recipeForm, recipe, db):
    # Get or create categories
    categories_set = set()
    for category_form in recipeForm.categories:
        if not category_form.category.data:
            raise Exception("Category can't be empty")
        categories_set.add(category_form.category.data)

    existing_categories = Categories.query.filter(Categories.name.in_(categories_set)).all()
    existing_categories_names = set(category.name for category in existing_categories)

    categories_list = []
    for category_name in categories_set:
        if category_name not in existing_categories_names:
            category = Categories(name=category_name)
            db.session.add(category)
            categories_list.append(category)
        else:
            category = next((c for c in existing_categories if c.name == category_name), None)
            categories_list.append(category)

    # Add categories to recipe
    recipe.categories = categories_list

    return recipe

def saveIngredients(recipeForm, recipe):
    ingredients = []
    for ingredient_form in recipeForm.ingredients:
        if (ingredient_form.ingredient.data == "" or ingredient_form.amount.data == "" or ingredient_form.unit.data == ""):
            raise Exception("Ingredient can't be empty")
        ingredient = RecipeIngredients(recipe_id=recipe.id, ingredient=ingredient_form.ingredient.data, amount=ingredient_form.amount.data, unit=ingredient_form.unit.data)
        ingredients.append(ingredient)
    
    return ingredients
def saveInstructions(recipeForm, recipe):
    instructions = []
    instruction_number = 1
    for instruction_form in recipeForm.instructions:
        if (instruction_form.instruction.data == ""):
            raise Exception("Instruction can't be empty")
        instruction = RecipeInstructions(recipe_id=recipe.id, instruction=instruction_form.instruction.data, instruction_number=instruction_number)
        instruction_number = instruction_number + 1
        instructions.append(instruction)
    
    return instructions


def saveRecipe(recipeForm, db, user_id):
    recipe = saveNameAndDesc(recipeForm, user_id)
    db.session.add(recipe)

    recipe = saveCategories(recipeForm, recipe, db)

    ingredients = saveIngredients(recipeForm, recipe)
    instructions = saveInstructions(recipeForm, recipe)

    db.session.bulk_save_objects(ingredients)
    db.session.bulk_save_objects(instructions)

    # Commit changes
    db.session.commit()

    return recipe