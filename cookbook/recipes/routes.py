from flask import Blueprint, render_template, redirect, flash, url_for, request, session, current_app
from flask_login import login_required, current_user
from cookbook.recipes.forms import RecipeForm, IngredientsForm, InstructionsForm, CategoriesForm, RecipeNameDescImage, RecipeCategories, RecipeIngredients, RecipeInstructions
from cookbook.models import Recipe, Categories, recipe_categories
from cookbook import db
from cookbook.recipes.services import saveRecipe, editRecipe
from cookbook.users.utils import recipe_id_check
from werkzeug.utils import secure_filename
import os
from cookbook.constants import MEASURING_UNITS

recipes = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes.route('/create_recipe/add_name_and_desc', methods=['GET', 'POST'])
@login_required
def add_name_and_desc():
    form = RecipeForm()
    if request.method == 'POST':
        # Store name and description in one session
        session['recipe_name'] = request.form['name']
        session['recipe_desc'] = request.form['description']

        # Store the image in a separate session
        file = request.files["images"]
        filename = secure_filename(file.filename)
        if (filename != ""):
            # save the image in a temporary folder so that if something happens, and the user doesn't finish the recipe, the image can be easily deleted later and not saved in the db
            file.save(os.path.join(current_app.static_folder + "/images/temp/", filename))
        session['recipe_image'] = filename

        return redirect(url_for('recipes.add_categories'))
    return render_template('recipe/add_recipe/add_name_and_desc.html', form=form)

@recipes.route('/create_recipe/add_categories', methods=['GET', 'POST'])
@login_required
def add_categories():
    form = RecipeForm()
    if request.method == 'POST':
        session['recipe_categories'] = form.categories.data
        return redirect(url_for('recipes.add_ingredients'))
    return render_template('recipe/add_recipe/add_categories.html', form=form)

@recipes.route('/create_recipe/add_ingredients', methods=['GET', 'POST'])
@login_required
def add_ingredients():
    form = RecipeForm()
    if request.method == 'POST':
        session['recipe_ingredients'] = form.ingredients.data
        return redirect(url_for('recipes.add_instructions'))
    return render_template('recipe/add_recipe/add_ingredients.html', form=form, measuring_units=MEASURING_UNITS)

@recipes.route('/create_recipe/add_instructions', methods=['GET', 'POST'])
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
        current_app.logger.error(e)
        return render_template("recipe/add_recipe/add_instructions.html", form=form, exception=e)
    

@recipes.route('/view_recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template("recipe/view_recipe.html", recipe=recipe)


@recipes.route('/edit_recipe/edit_name_and_desc/<int:id>', methods=['GET', 'POST'])
@login_required
@recipe_id_check(msg="edit", type="warning")
def edit_name_and_desc(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeNameDescImage()
    if form.validate_on_submit():
        # Save the form data to the session
        session['recipe_name'] = request.form['name']
        session['recipe_desc'] = request.form['description']

        # save the image to a temp folder, and in teh session save the image name
        file = request.files["images"]
        filename = secure_filename(file.filename)
        if (filename != ""):
            # save the image in a temporary folder so that if something happens, and the user doesn't finish the recipe, the image can be easily deleted later and not saved in the db
            file.save(os.path.join(current_app.static_folder + "/images/temp/", filename))
        session['recipe_image'] = filename

        # Redirect to the next page
        return redirect(url_for('recipes.edit_categories', id=recipe.id))
    else: # view the page OR if something went wrong with the form validation
        # Display the form with existing data
        form.name.data = recipe.name
        form.description.data = recipe.description
        return render_template("recipe/edit_recipe/edit_name_and_desc.html", form=form)


@recipes.route('/edit_recipe/edit_categories/<int:id>', methods=['GET', 'POST'])
@login_required
@recipe_id_check(msg="edit", type="warning")
def edit_categories(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeCategories()
    if form.validate_on_submit():      
        session['recipe_categories'] = form.categories.data
        return redirect(url_for('recipes.edit_ingredients', id=recipe.id))
    else: # view the page OR if something went wrong with the form validation
        categories_forms = []
        for entry in recipe.categories:
            categories_forms.append(CategoriesForm(category=entry.name))
        form.categories = categories_forms
        return render_template("recipe/edit_recipe/edit_categories.html", form=form)


@recipes.route('/edit_recipe/edit_ingredients/<int:id>', methods=['GET', 'POST'])
@login_required
@recipe_id_check(msg="edit", type="warning")
def edit_ingredients(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeIngredients()
    if form.validate_on_submit():
        session['recipe_ingredients'] = form.ingredients.data
        return redirect(url_for('recipes.edit_instructions', id=recipe.id))
    else: # view the page OR if something went wrong with the form validation
        current_app.logger.error(form.ingredients.errors)
        ingredients_forms = []
        for entry in recipe.recipe_ingredients:
            ingredients_forms.append(IngredientsForm(ingredient=entry.ingredient, amount=entry.amount, unit=entry.unit))
        form.ingredients = ingredients_forms
        return render_template("recipe/edit_recipe/edit_ingredients.html", form=form, measuring_units=MEASURING_UNITS)


@recipes.route('/edit_recipe/edit_instructions/<int:id>', methods=['GET', 'POST'])
@login_required
@recipe_id_check(msg="edit", type="warning")
def edit_instructions(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeInstructions()
    recipeForm = RecipeForm()
    if form.validate_on_submit():
        try:
            session['recipe_intructions'] = form.instructions.data
            recipeForm = editRecipe.fillRecipeForm(recipeForm)
            recipe = editRecipe.editRecipe(recipe, recipeForm, db)
            flash("Recipe has been updated", "success")
            return redirect(url_for('recipes.view_recipe', id=recipe.id))
        except Exception as e:
            current_app.logger.error(e)
            return render_template("recipe/edit_recipe/edit_instructions.html", form=form, exception=e)
    else: # view the page OR if something went wrong with the form validation
        instructions_forms = []
        for entry in recipe.recipe_instructions:
            instructions_forms.append(InstructionsForm(instruction=entry.instruction))
        form.instructions = instructions_forms
        return render_template("recipe/edit_recipe/edit_instructions.html", form=form)

@recipes.route('/delete_recipe/<int:id>', methods=['GET', 'POST'])
@login_required
@recipe_id_check(msg="delete", type="warning")
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        flash("Recipe Was Deleted!", "success")
    except:
        flash("Whoops! There was a problem deleting the recipe! Try again", "warning")
    finally:
        return redirect(url_for("main.home"))
    
@recipes.route('/view_my_recipes')
@login_required
def view_my_recipes():
    page = request.args.get('page', default=1, type=int)
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.date_added.desc()).paginate(page=page, per_page=2)

    return render_template("recipe/view_my_recipes.html", recipes=recipes)

@recipes.route('/view_recipes_by_category/<name>')
def view_recipes_by_category(name):
    recipes = Recipe.query.join(recipe_categories).join(Categories).filter(Categories.name == name).all()

    return render_template("recipe/view_recipes_by_category.html", recipes=recipes, category=name)