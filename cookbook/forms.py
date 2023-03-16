from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FieldList, DecimalField, FormField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from cookbook.models import Users

measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)"]

class LoginForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserRegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_hash', message="Passwords Must Match!")])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already Exists. Please choose another")

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
