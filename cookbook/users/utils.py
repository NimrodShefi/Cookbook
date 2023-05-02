from flask import redirect, flash, url_for
from flask_login import current_user
from flask_mail import Message
from functools import wraps
from cookbook import mail
from cookbook.models import Recipe

def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.", "info")
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)

    return decorated_function

def send_reset_email(user):
    token = user.get_reset_token()

    msg = Message(subject="Password Reset Request", sender='noreply@demo.com', recipients=[user.email])
    msg.body = f""" To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore the email, and no changes will be made
    
    """
    mail.send(msg)

def admin_check(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if (current_user.id != 1):
            flash("You don't permission to view this page", "danger")
            return redirect(url_for("main.home"))
        return func(*args, **kwargs)
    return decorated_function

def recipe_id_check(msg="", type="warning"):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = kwargs.get('id')
            recipe = Recipe.query.get_or_404(id)
            if (current_user.id != recipe.user_id):
                flash(f"You can only {msg} your own recipes", type)
                return redirect(url_for("main.home"))
            return func(*args, **kwargs)
        return decorated_function
    return decorator