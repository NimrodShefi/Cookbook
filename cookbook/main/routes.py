from flask import Blueprint, render_template, redirect, current_app
from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from cookbook.main.forms import SearchForm
from cookbook.models import Users, Recipe
from cookbook import db

main = Blueprint('main', __name__)

@main.route('/')
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

        with current_app.app_context():
            db.create_all()
            user_id_1 = Users.query.get(1)
            # If user with id 1 doesn't exists:
            if (user_id_1 is None):
                hashed_pw = generate_password_hash("123", "sha256")
                user = Users(name="Anonymous", email="example.email.com", password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()

    return redirect("/home")

# Pass Stuff To Navbar
@main.app_context_processor
def base():
    form = SearchForm()
    return dict(form=form)

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