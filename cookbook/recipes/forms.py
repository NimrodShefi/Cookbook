from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, DecimalField, FormField, SelectField
from wtforms.validators import DataRequired

measuring_units = ["grams (g)", "milligram (mg)", "kilogram (kg)", "milliliter (ml)", "liter (L)", "teaspoon (tsp)", "tablespoon (tbsp)", "cup", "pint", "gallon", "pound (lb)", "ounce (oz)", "Item"]

class IngredientsForm(FlaskForm):
    ingredient = StringField("Ingredient", validators=[DataRequired()])
    amount = DecimalField("Amount", validators=[DataRequired()])
    unit = SelectField("Units", choices=measuring_units, validators=[DataRequired()])

class InstructionsForm(FlaskForm):
    instruction = StringField("Instruction", validators=[DataRequired()])

class CategoriesForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired()])

class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientsForm), min_entries=1, validators=[DataRequired()])
    categories = FieldList(FormField(CategoriesForm), min_entries=1, validators=[DataRequired()])
    instructions = FieldList(FormField(InstructionsForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")