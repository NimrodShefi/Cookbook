from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from cookbook.models import Users
from flask_login import current_user


class LoginForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me", default=False)
    submit = SubmitField("Log in")

class UserRegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_hash', message="Passwords Must Match!")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already Exists. Please choose another")

class UserUpdateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_email(self, email):
        # Only run if the data is being updated
        if (email.data != current_user.email):
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email Already Exists. Please choose another")
            
class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email doesn't exists in the system")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords Must Match!")])
    submit = SubmitField("Update Password")