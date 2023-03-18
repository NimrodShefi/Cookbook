from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from cookbook.recipes.forms import RecipeForm, IngredientsForm, InstructionsForm
from cookbook.models import Recipe, RecipeIngredients, RecipeInstructions
from cookbook import db

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    user_id = current_user.id
    if (request.method == "POST"):
        recipe = Recipe(name=form.name.data, description=form.description.data, categories=form.categories.data, user_id=user_id)
        db.session.add(recipe)
        db.session.commit()
        for ingredient_form in form.ingredients:
            ingredient = RecipeIngredients(recipe_id=recipe.id, ingredient=ingredient_form.ingredient.data, amount=ingredient_form.amount.data, unit=ingredient_form.unit.data)
            db.session.add(ingredient)

        instruction_number = 1
        for instruction_form in form.instructions:
            instruction = RecipeInstructions(recipe_id=recipe.id, instruction=instruction_form.instruction.data, instruction_number=instruction_number)
            instruction_number = instruction_number + 1
            db.session.add(instruction)
        db.session.commit()
        form.process(formdata=None)
        flash("Recipe added successfully", "success")
        return redirect(url_for('recipes.view_recipe', id=recipe.id))
    return render_template("add_recipe.html", form=form)

@recipes.route('/recipes/view_recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template("view_recipe.html", recipe=recipe)

@recipes.route('/recipes/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    # When the user is trying to edit the recipe:
    if (request.method == "POST"):
        recipe.name = form.name.data 
        recipe.description = form.description.data

        # INGREDIENTS
        existing_recipe_ingredients = recipe.recipe_ingredients
        # There is the same amount of incoming ingredients as in the db
        if (len(form.ingredients) == len(existing_recipe_ingredients)):
            for i in range(len(form.ingredients)):
                recipe.recipe_ingredients[i].ingredient = form.ingredients[i].ingredient.data
                recipe.recipe_ingredients[i].amount = form.ingredients[i].amount.data
                recipe.recipe_ingredients[i].unit = form.ingredients[i].unit.data
        # There are more incoming ingredients then in the db
        elif (len(form.ingredients) > len(existing_recipe_ingredients)):
            for i in range(len(form.ingredients)):
                # As long as i looks at the ingredients in the db
                if (i < len(existing_recipe_ingredients)):
                    recipe.recipe_ingredients[i].ingredient = form.ingredients[i].ingredient.data
                    recipe.recipe_ingredients[i].amount = form.ingredients[i].amount.data
                    recipe.recipe_ingredients[i].unit = form.ingredients[i].unit.data
                # When it is the incoming ingredients that need to be created
                else:
                    ingredient = RecipeIngredients(recipe_id=recipe.id, ingredient=form.ingredients[i].ingredient.data, amount=form.ingredients[i].amount.data, unit=form.ingredients[i].unit.data)
                    db.session.add(ingredient)
        # There are less incoming ingredients then in the db
        else:
            for i in range(len(existing_recipe_ingredients)):
                # As long as i looks at the ingredients in the form
                if (i < len(form.ingredients)):
                    recipe.recipe_ingredients[i].ingredient = form.ingredients[i].ingredient.data
                    recipe.recipe_ingredients[i].amount = form.ingredients[i].amount.data
                    recipe.recipe_ingredients[i].unit = form.ingredients[i].unit.data
                # When there are more ingredients in the db than in the form
                else:
                    db.session.delete(recipe.recipe_ingredients[i])

        # INSTRUCTIONS
        existing_recipe_instructions = recipe.recipe_instructions
        # There is the same amount of incoming instructions as in the db
        if (len(form.instructions) == len(existing_recipe_instructions)):
            for i in range(len(form.instructions)):
                recipe.recipe_instructions[i].instruction_number = i + 1
                recipe.recipe_instructions[i].instruction = form.instructions[i].instruction.data
        # There are more incoming instructions then in the db
        elif (len(form.instructions) > len(existing_recipe_instructions)):
            for i in range(len(form.instructions)):
                # As long as i looks at the instructions in the db
                if (i < len(existing_recipe_instructions)):
                    recipe.recipe_instructions[i].instruction_number = i + 1
                    recipe.recipe_instructions[i].instruction = form.instructions[i].instruction.data
                # When it is the incoming instructions that need to be created
                else:
                    instruction = RecipeInstructions(recipe_id=recipe.id, instruction=form.instructions[i].instruction.data, instruction_number=i + 1)
                    db.session.add(instruction)
        # There are less incoming instructions then in the db
        else:
            for i in range(len(existing_recipe_instructions)):
                # As long as i looks at the instructions in the form
                if (i < len(form.instructions)):
                    recipe.recipe_instructions[i].instruction_number = i + 1
                    recipe.recipe_instructions[i].instruction = form.instructions[i].instruction.data
                # When there are more instructions in the db than in the form
                else:
                    db.session.delete(recipe.recipe_instructions[i])
                    
        recipe.categories = form.categories.data
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe has been updated", "success")
        return redirect(url_for('recipes.view_recipe', id=recipe.id))
    
    # When trying to view the page:
    if (current_user.id == recipe.user_id):
        ingredients_forms = []
        instructions_forms = []
        for entry in recipe.recipe_ingredients:
            ingredients_forms.append(IngredientsForm(ingredient=entry.ingredient, amount=entry.amount, unit=entry.unit))
        form.name.data = recipe.name
        form.description.data = recipe.description
        form.ingredients = ingredients_forms
        form.categories.data = recipe.categories
        for entry in recipe.recipe_instructions:
            instructions_forms.append(InstructionsForm(instruction=entry.instruction))
        form.instructions = instructions_forms
        measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)"]
        return render_template("edit_recipe.html", form=form, measuring_units=measuring_units)
    else:
        flash("You can only edit your own recipes", "warning")
        return redirect(url_for("main.home"))

@recipes.route('/recipes/delete_recipe/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    try:
        if (recipe_to_delete.user_id == current_user.id):
            db.session.delete(recipe_to_delete)
            db.session.commit()
            flash("Recipe Was Deleted!", "success")
        else:
            flash("You can only delete your own recipes", "danger")
    except:
        flash("Whoops! There was a problem deleting the recipe! Try again", "warning")
    finally:
        return redirect("/home")
    
@recipes.route('/recipes/view_my_recipes')
@login_required
def view_my_recipes():
    page = request.args.get('page', default=1, type=int)
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.date_added.desc()).paginate(page=page, per_page=2)

    return render_template("view_my_recipes.html", recipes=recipes)