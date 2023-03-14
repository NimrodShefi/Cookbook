from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FieldList, DecimalField, FormField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from flask_ckeditor import CKEditorField

measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)"]

# Login Form
class LoginForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Craete a User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message="Passwords Must Match!")])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class IngredientsForm(FlaskForm):
    ingredient = StringField("Ingredient", validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired()])
    unit = SelectField("Units", choices=measuring_units, validators=[DataRequired()])

class InstructionsForm(FlaskForm):
    instruction = StringField("Instruction", validators=[DataRequired()])

class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientsForm), min_entries=1, validators=[DataRequired()])
    categories = StringField("Categories", validators=[DataRequired()])
    instructions = FieldList(FormField(InstructionsForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched =  StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
