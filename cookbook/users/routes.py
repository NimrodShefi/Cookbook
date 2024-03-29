from flask import Blueprint, render_template, redirect, flash, url_for, request, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from cookbook.users.forms import LoginForm, UserRegistrationForm, UserUpdateForm, RequestResetForm, ResetPasswordForm, AdminUserEditForm
from cookbook.models import Users, Recipe
from cookbook import db, login_manger
from cookbook.users.utils import logout_required, send_reset_email
from cookbook.users.utils import admin_check
from datetime import timedelta

users = Blueprint('users', __name__)

@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@users.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            # Set the session duration based on the "remember me" checkbox
            if form.remember.data:
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(weeks=1)
            else:
                session.permanent = False
                current_app.permanent_session_lifetime = timedelta(hours=12)
            login_user(user)
            # If the user tried to access a page that needed login before being able to access
            next_page = request.args.get('next') # this is like args[''] however, if args is empty, instead of an error, it will just return None
            flash("Login Successfull", "success")
            # This is an if statement in one line 
            #       redirect to next_page if exists   else redirect to the home page
            return redirect(next_page) if (next_page) else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please check the email and password", "danger")
    return render_template("user/login.html", form=form)

@users.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    name = None
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully", "success")
        return redirect(url_for("users.login"))
    return render_template("user/register.html",name=name, form=form)

@users.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have been Logged Out!", "success")
    return redirect(url_for('users.login'))

@users.route('/settings' , methods=['GET', 'POST'])
@login_required
def settings():
    userUpdateForm = UserUpdateForm()
    changePasswordForm = ResetPasswordForm()
    user = Users.query.get_or_404(current_user.id)
    if (userUpdateForm.validate_on_submit()):
        user.name = userUpdateForm.name.data
        user.email = userUpdateForm.email.data
        db.session.commit()
        flash("User Updated", "success")
        return redirect(url_for('users.settings'))
    if (changePasswordForm.validate_on_submit()):
        hashed_pw = generate_password_hash(changePasswordForm.password.data, "sha256")
        user.password_hash = hashed_pw
        db.session.commit()
        flash("Password Updated", "success")
        return redirect(url_for('users.settings'))
    if (request.method == "GET"):
        userUpdateForm.name.data = user.name
        userUpdateForm.email.data = user.email
        return render_template("user/settings.html", userUpdateForm=userUpdateForm, changePasswordForm=changePasswordForm)
    
@users.route('/reset_password', methods=["POST", "GET"])
@logout_required
def reset_request():
    form = RequestResetForm()
    if (current_user.is_authenticated):
        return redirect(url_for('main.home'))
    if (request.method == "POST"):
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("Email doesn't exists in the system", "danger")
            return redirect(url_for('users.reset_request'))
        send_reset_email(user)
        flash("An email has been sent to reset your password", "info")
        return redirect(url_for("users.login"))
    return render_template("user/reset_request.html", title="Reset Password", form=form)

@users.route('/reset_password/<token>', methods=["POST", "GET"])
@logout_required
def reset_token(token):
    if (current_user.is_authenticated):
        return redirect(url_for('main.home'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            # Hash the password
            hashed_pw = generate_password_hash(form.password.data, "sha256")
            user.password_hash = hashed_pw
            db.session.commit()
            flash("Your password has been updated!", "success")
            return redirect(url_for("users.login"))
        return render_template("user/reset_token.html", title="Reset Password", form=form)

@users.route('/users/delete_user/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_user(id):
    user_to_delete = Users.query.get(id)
    user_admin = Users.query.get(1) # This is a user that gets automatically added when the db is created
    recipes_belonging_to_user = Recipe.query.filter_by(user_id=current_user.id)
    try:
        if (user_to_delete.id == current_user.id):
            for recipe in recipes_belonging_to_user:
                recipe.user = user_admin
            logout_user()
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Was Deleted!", "success")
        else:
            flash("You can only delete your own user", "danger")
    except:
        flash("Whoops! There was a problem deleting the user! Try again", "warning")
    finally:
        return redirect(url_for('main.home'))
    
@users.route('/users/admin', methods=['GET'])
@login_required
@admin_check
def admin():
    users = Users.query.all()
    users.pop(0)
    return render_template("user/admin/view_all_users.html", users=users)

@users.route('/users/admin/<int:id>', methods=['GET', 'POST'])            
@login_required
@admin_check
def edit_user(id):
    user_to_edit = Users.query.get(id)
    form = AdminUserEditForm()
    if (request.method == "GET"):
        if (id == 1):
            flash("Not allowed to edit this user details", "warning")
            return redirect(url_for('users.admin'))
        form.id.data = user_to_edit.id
        form.name.data = user_to_edit.name
        form.email.data = user_to_edit.email
        return render_template("user/admin/edit_user.html", user=user_to_edit, form=form)
    
    if (request.method == "POST"):
        user = Users.query.filter_by(id=form.id.data).first()
        if user:
            flash("User already has this id. Choose another one.", "warning")
            return redirect(url_for('users.edit_user', id=id))
        user_to_edit.id = form.id.data
        user_to_edit.name = form.name.data
        user_to_edit.email = form.email.data
        db.session.commit()
        flash("User details updated!", "success")
        return redirect(url_for('users.admin'))
