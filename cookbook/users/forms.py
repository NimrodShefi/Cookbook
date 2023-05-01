from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError, Regexp
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
    password_hash = PasswordField('Password', validators=[
        DataRequired(message="Must have a value"),
        Length(min=8, message="At least 8 characters long"),
        Regexp('.*[A-Z].*', message="At least one uppercase letter"),
        Regexp('.*[a-z].*', message="At least one lowercase letter"),
        Regexp('.*[1-9].*', message="At least one number"),
        Regexp('.*[!@#$%^&*()].*', message="At least one special character")
    ], id="password")
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_hash', message="Passwords Must Match!")], id="confirmPassword")
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
    password = PasswordField('Password', validators=[
        DataRequired(message="Must have a value"),
        Length(min=8, message="At least 8 characters long"),
        Regexp('.*[A-Z].*', message='At least one uppercase letter'),
        Regexp('.*[a-z].*', message='At least one lowercase letter'),
        Regexp('.*[1-9].*', message='At least one number'),
        Regexp('.*[!@#$%^&*()].*', message='At least one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords Must Match!")])
    submit = SubmitField("Update Password")