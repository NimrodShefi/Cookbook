from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from flask_migrate import Migrate
from webforms import LoginForm, UserForm, RecipeForm, SearchForm, IngredientsForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_ckeditor import CKEditor

# CONFIG
app = Flask(__name__)
# Secret Key
app.config["SECRET_KEY"] = "mysecretkey"
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123654@localhost/my_cookbook"
# CKEditor
ckeditor = CKEditor(app)
# Initialise The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# need to import the models after setting up the db becuase if not, the db varaible in models will not be initialised yet
from models import Users, Recipe, RecipeIngredients

## Flask Login Manager
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'

@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Pass Stuff To Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Create Search Funtion
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    recipes = Recipe.query
    if (form.validate_on_submit()):
        searched = form.searched.data
        # Checking whether the searched for information is in description or name
        recipes = recipes.filter(or_(Recipe.description.like('%' + searched + '%'), Recipe.name.like('%' + searched + '%')))
        recipes = recipes.order_by(Recipe.name).all()
        return render_template("search.html", form=form, searched=searched, recipes=recipes)

# CONTROLLERS
@app.route('/')
def index():
    return redirect("/home")

@app.route('/home')
def home():
    recipes = Recipe.query.order_by(desc(Recipe.date_added)).limit(5)
    return render_template("home.html", recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                # check the passowrd hash
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Login Successfull")
                    return redirect(url_for('home'))
                else:
                    flash("Wrong Password. Try Again!")
            else:
                flash("User Doesn't Exist. Try Again!")
        return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if (current_user.is_authenticated):
        return redirect(url_for('home'))
    else:
        name = None
        form = UserForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None:
                # Hash the password
                hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
                user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.email.data = ''
            form.password_hash.data = ''
            flash("User Added Successfully")
        return render_template("register.html",name=name, form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have been Logged Out!")
    return redirect(url_for('login'))

@app.route('/recipes/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    user_id = current_user.id
    if (request.method == "POST"):
        recipe = Recipe(name=form.name.data, description=form.description.data, instructions=form.instructions.data, categories=form.categories.data, user_id=user_id)
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id
        for ingredient_form in form.ingredients:
            ingredient = RecipeIngredients(recipe_id=recipe_id, ingredient=ingredient_form.ingredient.data, amount=ingredient_form.amount.data, unit=ingredient_form.unit.data)
            db.session.add(ingredient)
        db.session.commit()
        form.process(formdata=None)
        flash("Recipe added successfully")
    return render_template("add_recipe.html", form=form)

@app.route('/recipes/view_recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template("view_recipe.html", recipe=recipe)

@app.route('/recipes/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()
    # When the user is trying to edit the recipe:
    if (request.method == "POST"):
        recipe.name = form.name.data 
        recipe.description = form.description.data
        # Delete every ingredient from the db before
        for entry in recipe.recipe_ingredients:
            db.session.delete(entry)
        # Adding it back again in the updated form again
        for ingredient_form in form.ingredients:
            ingredient = RecipeIngredients(recipe_id=recipe.id, ingredient=ingredient_form.ingredient.data, amount=ingredient_form.amount.data, unit=ingredient_form.unit.data)
            db.session.add(ingredient)
        recipe.categories = form.categories.data
        recipe.instructions = form.instructions.data
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe has been updated")
        return redirect(url_for('view_recipe', id=recipe.id))
    # When trying to view the page:
    if (current_user.id == recipe.user_id):
        ingredients_forms = []
        for entry in recipe.recipe_ingredients:
            ingredients_forms.append(IngredientsForm(ingredient=entry.ingredient, amount=entry.amount, unit=entry.unit))
        form.name.data = recipe.name
        form.description.data = recipe.description
        form.ingredients = ingredients_forms
        form.categories.data = recipe.categories
        form.instructions.data = recipe.instructions
        measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)"]
        return render_template("edit_recipe.html", form=form, measuring_units=measuring_units)
    else:
        flash("You can only edit your own recipes")
        return redirect(url_for("home"))

@app.route('/recipes/delete_recipe/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    try:
        if (recipe_to_delete.user_id == current_user.id):
            db.session.delete(recipe_to_delete)
            db.session.commit()
            flash("Recipe Was Deleted!")
        else:
            flash("You can only delete your own recipes")
    except:
        flash("Whoops! There was a problem deleting the recipe! Try again")
    finally:
        return redirect("/home")
    
@app.route('/recipes/view_my_recipes/<int:id>')
@login_required
def view_my_recipes(id):
    recipes = Recipe.query.filter(Recipe.user_id)
    recipes = recipes.order_by(desc(Recipe.date_added)).all()
    my_recipes = []
    for recipe in recipes:
        if (recipe.user_id == id):
            my_recipes.append(recipe)
    return render_template("view_my_recipes.html", recipes=my_recipes)
    
# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error_type="404 Error", error_msg="Page Not Found - Try Again..."), 404

# Inernal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("error.html", error_type="500 Internal Server Error", error_msg="Something Went Wrong !Try Again..."), 500
