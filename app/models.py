from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    recipe = db.relationship('Recipe', backref='recipe')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    categories = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    recipe_ingredients = db.relationship('RecipeIngredients', backref='recipe_ingredients') 
    recipe_instructions = db.relationship('RecipeInstructions', backref='recipe_instructions') 

class RecipeIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.DECIMAL(precision=6, scale=2), nullable=False)
    unit = db.Column(db.String(255), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class RecipeInstructions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instruction_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text(), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
