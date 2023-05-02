from flask import Blueprint, render_template, redirect, flash, url_for, request, session, current_app
from flask_login import login_required, current_user
from cookbook.recipes.forms import RecipeForm, IngredientsForm, InstructionsForm, CategoriesForm
from cookbook.models import Recipe, Categories, recipe_categories
from cookbook import db
from cookbook.recipes.services import saveRecipe, editRecipe


recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes/create_recipe/add_name_and_desc', methods=['GET', 'POST'])
@login_required
def add_name_and_desc():
    form = RecipeForm()
    if request.method == 'POST':
        session['recipe_name_and_desc'] = request.form
        return redirect(url_for('recipes.add_ingredients'))
    return render_template('recipe/add_recipe/add_name_and_desc.html', form=form)

@recipes.route('/recipes/create_recipe/add_ingredients', methods=['GET', 'POST'])
@login_required
def add_ingredients():
    form = RecipeForm()
    if request.method == 'POST':
        session['recipe_ingredients'] = form.ingredients.data
        return redirect(url_for('recipes.add_categories'))
    return render_template('recipe/add_recipe/add_ingredients.html', form=form)

@recipes.route('/recipes/create_recipe/add_categories', methods=['GET', 'POST'])
@login_required
def add_categories():
    form = RecipeForm()
    if request.method == 'POST':
        session['recipe_categories'] = form.categories.data
        return redirect(url_for('recipes.add_instructions'))
    return render_template('recipe/add_recipe/add_categories.html', form=form)

@recipes.route('/recipes/create_recipe/add_instructions', methods=['GET', 'POST'])
@login_required
def add_instructions():
    try:
        form = RecipeForm()
        if request.method == 'POST':
            form = saveRecipe.fillRecipeForm(form)
            # Saving the data in the variable form into the db using the saveRecipe function
            user_id = current_user.id
            recipe = saveRecipe.saveRecipe(form, db, user_id)
            flash('Recipe added successfully', 'success')
            return redirect(url_for('recipes.view_recipe', id=recipe.id))
        return render_template('recipe/add_recipe/add_instructions.html', form=form)
    except Exception as e:
        return render_template("recipe/add_recipe/add_instructions.html", form=form, exception=e)
    

@recipes.route('/recipes/view_recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template("recipe/view_recipe.html", recipe=recipe)


@recipes.route('/recipes/edit_recipe/edit_name_and_desc/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_name_and_desc(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    if (request.method == "POST"):
        session['recipe_name_and_desc'] = request.form
        return redirect(url_for('recipes.edit_ingredients', id=recipe.id))
    if (current_user.id == recipe.user_id):
        form.name.data = recipe.name
        form.description.data = recipe.description
        return render_template("recipe/edit_recipe/edit_name_and_desc.html", form=form)
    else:
        flash("You can only edit your own recipes", "warning")
        return redirect(url_for("main.home"))

@recipes.route('/recipes/edit_recipe/edit_ingredients/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ingredients(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)", "Item"]
    if request.method == 'POST':
        session['recipe_ingredients'] = form.ingredients.data
        return redirect(url_for('recipes.edit_categories', id=recipe.id))
    if (current_user.id == recipe.user_id):
        ingredients_forms = []
        for entry in recipe.recipe_ingredients:
            ingredients_forms.append(IngredientsForm(ingredient=entry.ingredient, amount=entry.amount, unit=entry.unit))
        form.ingredients = ingredients_forms
        return render_template("recipe/edit_recipe/edit_ingredients.html", form=form, measuring_units=measuring_units)
    else:
        flash("You can only edit your own recipes", "warning")
        return redirect(url_for("main.home"))

@recipes.route('/recipes/edit_recipe/edit_categories/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_categories(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    if request.method == 'POST':
        session['recipe_categories'] = form.categories.data
        return redirect(url_for('recipes.edit_instructions', id=recipe.id))
    if (current_user.id == recipe.user_id):
        categories_forms = []
        for entry in recipe.categories:
            categories_forms.append(CategoriesForm(category=entry.name))
        form.categories = categories_forms
        return render_template("recipe/edit_recipe/edit_categories.html", form=form)
    else:
        flash("You can only edit your own recipes", "warning")
        return redirect(url_for("main.home"))

@recipes.route('/recipes/edit_recipe/edit_instructions/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_instructions(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    if (request.method=="POST"):
        try:
            form = editRecipe.fillRecipeForm(form)
            recipe = editRecipe.editRecipe(recipe, form, db)
            flash("Recipe has been updated", "success")
            return redirect(url_for('recipes.view_recipe', id=recipe.id))
        except Exception as e:
            return render_template("recipe/edit_recipe/edit_instructions.html", form=form, exception=e)
    if (current_user.id == recipe.user_id):
        instructions_forms = []
        for entry in recipe.recipe_instructions:
            instructions_forms.append(InstructionsForm(instruction=entry.instruction))
        form.instructions = instructions_forms
        return render_template("recipe/edit_recipe/edit_instructions.html", form=form)
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

    return render_template("recipe/view_my_recipes.html", recipes=recipes)

@recipes.route('/recipes/view_recipes_by_category/<name>')
def view_recipes_by_category(name):
    recipes = Recipe.query.join(recipe_categories).join(Categories).filter(Categories.name == name).all()

    return render_template("recipe/view_recipes_by_category.html", recipes=recipes)