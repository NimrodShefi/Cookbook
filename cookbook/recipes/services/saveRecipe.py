from cookbook.models import Recipe, RecipeIngredients, RecipeInstructions, Categories, RecipeImages
from flask import session, current_app
from cookbook.recipes.forms import IngredientsForm, CategoriesForm
import os
import uuid
from PIL import Image

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

def saveImage(recipeForm, recipe):
    filename = recipeForm.images.data
    random_string = str(uuid.uuid4())

    recipe_images_folder_path = f"{current_app.static_folder}/images/recipes"
    if not os.path.exists(recipe_images_folder_path):
        os.makedirs(recipe_images_folder_path)

    # Retrieve the image from the temp folder
    image = Image.open(f"{current_app.static_folder}/images/temp/{filename}")

    # Add the random string to the beginning of the filename
    new_filename = random_string + '_' + filename

    # Save the image in the proper location with a more secure name
    image.save(os.path.join(current_app.static_folder + "/images/recipes/", new_filename))
    # Remove the image from the temp folder
    os.remove(f"{current_app.static_folder}/images/temp/{filename}")
    
    return RecipeImages(recipe_id=recipe.id, image=new_filename)

def saveRecipe(recipeForm, db, user_id):
    recipe = saveNameAndDesc(recipeForm, user_id)
    db.session.add(recipe)

    recipe = saveCategories(recipeForm, recipe, db)

    # Run only if there is an acutal image uploaded
    if (recipeForm.images.data != ""):
        image = saveImage(recipeForm, recipe)
        db.session.add(image)

    ingredients = saveIngredients(recipeForm, recipe)
    instructions = saveInstructions(recipeForm, recipe)

    db.session.bulk_save_objects(ingredients)
    db.session.bulk_save_objects(instructions)

    # Commit changes
    db.session.commit()

    return recipe

def fillRecipeForm(recipeForm):
    # collecting the information stored in a session --> Instructions are not in a session, as they were just collected, and in the form
    recipe_name = session.get('recipe_name', {})
    recipe_desc = session.get('recipe_desc', {})
    recipe_ingredients = session.get('recipe_ingredients', [])
    recipe_categories = session.get('recipe_categories', [])
    recipe_image_name = session.get('recipe_image', [])
    # using the data from the session, to fill the missing gaps in the RecipeForm
    recipeForm.name.data = recipe_name
    recipeForm.description.data = recipe_desc
    recipeForm.ingredients.entries = [IngredientsForm(**i) for i in recipe_ingredients]
    recipeForm.categories.entries = [CategoriesForm(**c) for c in recipe_categories]
    recipeForm.images.data = recipe_image_name

    return recipeForm