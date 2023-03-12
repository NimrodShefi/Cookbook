from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, FieldList, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_ckeditor import CKEditorField

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

class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    ingridients = CKEditorField("Ingridients", validators=[DataRequired()])
    categories = StringField("Categories", validators=[DataRequired()])
    instructions = CKEditorField("Instructions", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched =  StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
