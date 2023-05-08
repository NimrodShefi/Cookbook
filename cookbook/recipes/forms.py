from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, DecimalField, FormField, SelectField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, ValidationError
from cookbook.constants import MEASURING_UNITS

class IngredientsForm(FlaskForm):
    ingredient = StringField("Ingredient", render_kw={"placeholder": "Butter"}, validators=[DataRequired(message="Ingredient can't be empty")])
    amount = DecimalField("Amount", render_kw={"placeholder": "100"}, validators=[DataRequired(message="The ingredient must have an amount")])
    unit = SelectField("Units", choices=MEASURING_UNITS, validators=[DataRequired()])

    def validate_amount_type(self, amount):
        if (not amount.isnumeric()):
            raise ValidationError("Amount must be a number")

class InstructionsForm(FlaskForm):
    instruction = StringField("Instruction", render_kw={"placeholder": "Whip the butter"}, validators=[DataRequired(message="Instruction can't be empty")])

class CategoriesForm(FlaskForm):
    category = StringField("Category", render_kw={"placeholder": "Pastry"}, validators=[DataRequired(message="Cateogry can't be empty")])

class RecipeNameDescImage(FlaskForm):
    name = StringField("Recipe Name", render_kw={"placeholder": "Croissants"}, validators=[DataRequired()])
    description = StringField("Description", render_kw={"placeholder": "A buttery, crescent-shaped French pastry"}, validators=[DataRequired()])
    images = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images Only!")])
    submit = SubmitField("Submit")

class RecipeCategories(FlaskForm):
    categories = FieldList(FormField(CategoriesForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")

class RecipeIngredients(FlaskForm):
    ingredients = FieldList(FormField(IngredientsForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")

class RecipeInstructions(FlaskForm):
    instructions = FieldList(FormField(InstructionsForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")

class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", render_kw={"placeholder": "Croissants"}, validators=[DataRequired()])
    description = StringField("Description", render_kw={"placeholder": "A buttery, crescent-shaped French pastry"}, validators=[DataRequired()])
    images = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images Only!")])
    categories = FieldList(FormField(CategoriesForm), min_entries=1, validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientsForm), min_entries=1, validators=[DataRequired()])
    instructions = FieldList(FormField(InstructionsForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")
