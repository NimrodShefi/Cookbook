from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from webforms import LoginForm, UserForm, RecipeForm
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
from models import Users, Recipe

## Flask Login Manager
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'

@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# CONTROLLERS
@app.route('/')
def index():
    return redirect("/home")

@app.route('/home')
def home():
    recipes = Recipe.query.order_by(Recipe.id)
    return render_template("home.html", recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    if form.validate_on_submit():
        recipe = Recipe(name=form.title.data, description=form.description.data, ingridients=form.ingridients.data, instructions=form.instructions.data, categories=form.categories.data)
        db.session.add(recipe)
        db.session.commit()
        form.title.data = ''
        form.description.data = ''
        form.ingridients.data = ''
        form.categories.data = ''
        form.instructions.data = ''
        flash("Recipe added successfully")
    return render_template("add_recipe.html", form=form)

@app.route('/recipes/view_recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template("view_recipe.html", recipe=recipe)

@app.route('/recipes/delete_recipe/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        flash("Recipe Was Deleted!")
    except:
        flash("Whoops! There was a problem deleting the recipe! Try again")
    finally:
        return redirect("/home")