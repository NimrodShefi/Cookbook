from flask import session, current_app
from cookbook.recipes.forms import IngredientsForm, CategoriesForm, InstructionsForm
from cookbook.models import RecipeIngredients, RecipeInstructions, Categories, RecipeImages
import os
import uuid
from PIL import Image

def editNameAndDescription(recipeForm, recipe):
    if recipeForm.name.data == "":
        raise Exception("Recipe name can't be empty")
    elif recipeForm.description.data == "":
        raise Exception("Recipe description can't be empty")
    recipe.name = recipeForm.name.data 
    recipe.description = recipeForm.description.data

    return recipe

def editIngredients(recipeForm, recipe, db):
    for ingredient in recipeForm.ingredients:
        if(ingredient.ingredient.data == "" or ingredient.amount.data == "" or ingredient.unit.data == ""):
            raise Exception("Ingredient can't be empty")

    existing_recipe_ingredients = recipe.recipe_ingredients
    # There is the same amount of incoming ingredients as in the db
    if (len(recipeForm.ingredients) == len(existing_recipe_ingredients)):
        for i in range(len(recipeForm.ingredients)):
            recipe.recipe_ingredients[i].ingredient = recipeForm.ingredients[i].ingredient.data
            recipe.recipe_ingredients[i].amount = recipeForm.ingredients[i].amount.data
            recipe.recipe_ingredients[i].unit = recipeForm.ingredients[i].unit.data
    # There are more incoming ingredients then in the db
    elif (len(recipeForm.ingredients) > len(existing_recipe_ingredients)):
        for i in range(len(recipeForm.ingredients)):
            # As long as i looks at the ingredients in the db
            if (i < len(existing_recipe_ingredients)):
                recipe.recipe_ingredients[i].ingredient = recipeForm.ingredients[i].ingredient.data
                recipe.recipe_ingredients[i].amount = recipeForm.ingredients[i].amount.data
                recipe.recipe_ingredients[i].unit = recipeForm.ingredients[i].unit.data
            # When it is the incoming ingredients that need to be created
            else:
                ingredient = RecipeIngredients(recipe_id=recipe.id, ingredient=recipeForm.ingredients[i].ingredient.data, amount=recipeForm.ingredients[i].amount.data, unit=recipeForm.ingredients[i].unit.data)
                db.session.add(ingredient)
    # There are less incoming ingredients then in the db
    else:
        for i in range(len(existing_recipe_ingredients)):
            # As long as i looks at the ingredients in the form
            if (i < len(recipeForm.ingredients)):
                recipe.recipe_ingredients[i].ingredient = recipeForm.ingredients[i].ingredient.data
                recipe.recipe_ingredients[i].amount = recipeForm.ingredients[i].amount.data
                recipe.recipe_ingredients[i].unit = recipeForm.ingredients[i].unit.data
            # When there are more ingredients in the db than in the form
            else:
                db.session.delete(recipe.recipe_ingredients[i])

    return recipe

def editInstructions(recipeForm, recipe, db):
    for instruction in recipeForm.instructions:
        if(instruction.instruction.data == ""):
            raise Exception("Instruction can't be empty")

    existing_recipe_instructions = recipe.recipe_instructions
    # There is the same amount of incoming instructions as in the db
    if (len(recipeForm.instructions) == len(existing_recipe_instructions)):
        for i in range(len(recipeForm.instructions)):
            recipe.recipe_instructions[i].instruction_number = i + 1
            recipe.recipe_instructions[i].instruction = recipeForm.instructions[i].instruction.data
    # There are more incoming instructions then in the db
    elif (len(recipeForm.instructions) > len(existing_recipe_instructions)):
        for i in range(len(recipeForm.instructions)):
            # As long as i looks at the instructions in the db
            if (i < len(existing_recipe_instructions)):
                recipe.recipe_instructions[i].instruction_number = i + 1
                recipe.recipe_instructions[i].instruction = recipeForm.instructions[i].instruction.data
            # When it is the incoming instructions that need to be created
            else:
                instruction = RecipeInstructions(recipe_id=recipe.id, instruction=recipeForm.instructions[i].instruction.data, instruction_number=i + 1)
                db.session.add(instruction)
    # There are less incoming instructions then in the db
    else:
        for i in range(len(existing_recipe_instructions)):
            # As long as i looks at the instructions in the form
            if (i < len(recipeForm.instructions)):
                recipe.recipe_instructions[i].instruction_number = i + 1
                recipe.recipe_instructions[i].instruction = recipeForm.instructions[i].instruction.data
            # When there are more instructions in the db than in the form
            else:
                db.session.delete(recipe.recipe_instructions[i])
    
    return recipe

def editCategories(recipeForm, recipe):
    for category in recipeForm.categories:
        if(category.category.data == ""):
            raise Exception("Category can't be empty")

    recipe.categories.clear()   
    for entry in recipeForm.categories:
        category = Categories.query.filter_by(name=entry.category.data).first()
        if not category:
            category = Categories(name=entry.category.data)
        recipe.categories.append(category)
    
    return recipe

def editImage(recipeForm, recipe):
    filename = recipeForm.images.data
    random_string = str(uuid.uuid4())

    # Get name of old image which will get deleted
    old_image = RecipeImages.query.filter_by(recipe_id = recipe.id).first()

    # Retrieve the image from the temp folder
    new_image = Image.open(f"{current_app.static_folder}/images/temp/{filename}")

    # Add the random string to the beginning of the filename
    new_filename = random_string + '_' + filename

    # Save the image in the proper location with a more secure name
    new_image.save(os.path.join(current_app.static_folder + "/images/recipes/", new_filename))
    # Remove the image from the temp folder
    os.remove(f"{current_app.static_folder}/images/temp/{filename}")
    
    if (old_image is not None):
        # Remove the old image from the folder
        old_image_name = old_image.image
        os.remove(f"{current_app.static_folder}/images/recipes/{old_image_name}")
        old_image.image = new_filename
        return old_image
    else:
        # Create a new RecipeImages object if there was no old image
        new_recipe_image = RecipeImages(recipe_id=recipe.id, image=new_filename)
        return new_recipe_image

def editRecipe(recipe, recipeForm, db):
    editNameAndDescription(recipeForm, recipe)
    editIngredients(recipeForm, recipe, db)
    editInstructions(recipeForm, recipe, db)
    editCategories(recipeForm, recipe)

    # Run only if there is an acutal image uploaded
    if (recipeForm.images.data != ""):
        image = editImage(recipeForm, recipe)
        db.session.add(image)
    
    db.session.add(recipe)
    db.session.commit()

    return recipe

def fillRecipeForm(recipeForm):
    # collecting the information stored in the session
    recipe_name = session.get('recipe_name', {})
    recipe_desc = session.get('recipe_desc', {})
    recipe_ingredients = session.get('recipe_ingredients', [])
    recipe_categories = session.get('recipe_categories', [])
    recipe_intructions = session.get('recipe_intructions', [])
    recipe_image_name = session.get('recipe_image', [])
    # using the data from the session, to fill the missing gaps in the RecipeForm
    recipeForm.name.data = recipe_name
    recipeForm.description.data = recipe_desc
    recipeForm.ingredients.entries = [IngredientsForm(**i) for i in recipe_ingredients]
    recipeForm.categories.entries = [CategoriesForm(**c) for c in recipe_categories]
    recipeForm.instructions.entries = [InstructionsForm(**i) for i in recipe_intructions]
    recipeForm.images.data = recipe_image_name


    return recipeForm