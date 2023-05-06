from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, DecimalField, FormField, SelectField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired
from cookbook.constants import MEASURING_UNITS

class IngredientsForm(FlaskForm):
    ingredient = StringField("Ingredient", render_kw={"placeholder": "Butter"}, validators=[DataRequired()])
    amount = DecimalField("Amount", render_kw={"placeholder": "100"}, validators=[DataRequired()])
    unit = SelectField("Units", choices=MEASURING_UNITS, validators=[DataRequired()])

class InstructionsForm(FlaskForm):
    instruction = StringField("Instruction", render_kw={"placeholder": "Whip the butter"}, validators=[DataRequired()])

class CategoriesForm(FlaskForm):
    category = StringField("Category", render_kw={"placeholder": "Pastry"}, validators=[DataRequired()])

class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", render_kw={"placeholder": "Croissants"}, validators=[DataRequired()])
    description = StringField("Description", render_kw={"placeholder": "A buttery, crescent-shaped French pastry"}, validators=[DataRequired()])
    # images = MultipleFileField("Images", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images only!")], name="images")
    images = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images Only!")])
    ingredients = FieldList(FormField(IngredientsForm), min_entries=1, validators=[DataRequired()])
    categories = FieldList(FormField(CategoriesForm), min_entries=1, validators=[DataRequired()])
    instructions = FieldList(FormField(InstructionsForm), min_entries=1, validators=[DataRequired()])
    submit = SubmitField("Submit")
