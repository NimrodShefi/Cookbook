from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from flask_migrate import Migrate
from webforms import LoginForm, UserForm, RecipeForm, SearchForm, IngredientsForm, InstructionsForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
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
from models import Users, Recipe, RecipeIngredients, RecipeInstructions

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
    # This makes sure that I can easily recreate the db, while also adding a default user which I would know what his user id is every time without worry
    import mysql.connector
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123654"
    )

    my_cursor = mydb.cursor()
    my_cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in my_cursor.fetchall()]
    if 'my_cookbook' not in databases:
        my_cursor.execute("CREATE DATABASE my_cookbook")

        with app.app_context():
            db.create_all()
            user_id_1 = Users.query.get(1)
            # If user with id 1 doesn't exists:
            if (user_id_1 is None):
                hashed_pw = generate_password_hash("123", "sha256")
                user = Users(name="Anonymous", email="example.email.com", password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()

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
        recipe = Recipe(name=form.name.data, description=form.description.data, categories=form.categories.data, user_id=user_id)
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id
        for ingredient_form in form.ingredients:
            ingredient = RecipeIngredients(recipe_id=recipe_id, ingredient=ingredient_form.ingredient.data, amount=ingredient_form.amount.data, unit=ingredient_form.unit.data)
            db.session.add(ingredient)

        instruction_number = 1
        for instruction_form in form.instructions:
            instruction = RecipeInstructions(recipe_id=recipe_id, instruction=instruction_form.instruction.data, instruction_number=instruction_number)
            instruction_number = instruction_number + 1
            db.session.add(instruction)
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
        flash("Recipe has been updated")
        return redirect(url_for('view_recipe', id=recipe.id))
    
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
