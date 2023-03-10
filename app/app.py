from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from webforms import LoginForm, UserForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
# Secret Key
app.config["SECRET_KEY"] = "mysecretkey"
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123654@localhost/my_cookbook" # --> New MySQL DB
# Initialise The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Flask Login Manager
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'

@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            # check the passowrd hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull")
                return redirect(url_for('home'))
            else:
                flash("Wrong Password. Try Again!")
        else:
            flash("User Doesn't Exist. Try Again!")
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    name = None
    form = UserForm()
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
        flash("User Added Successfully")
    return render_template("register.html",name=name, form=form)

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    # Password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name