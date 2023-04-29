from flask import Blueprint, render_template, redirect
from sqlalchemy import or_
from cookbook.main.forms import SearchForm
from cookbook.models import Recipe, Categories

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect("/home")

# Pass Stuff To Navbar
@main.app_context_processor
def base():
    form = SearchForm()
    categories = Categories.query.all()
    return dict(form=form, categories=categories)

# Create Search Funtion
@main.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    recipes = Recipe.query
    if (form.validate_on_submit()):
        searched = form.searched.data
        # Checking whether the searched for information is in description or name
        recipes = recipes.filter(or_(Recipe.description.like('%' + searched + '%'), Recipe.name.like('%' + searched + '%')))
        recipes = recipes.order_by(Recipe.name).all()
        return render_template("search.html", form=form, searched=searched, recipes=recipes)

@main.route('/home')
def home():
    recipes = Recipe.query.order_by(Recipe.date_added.desc()).limit(5)
    return render_template("home.html", recipes=recipes)