from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from food_parser import get_food_data
from forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, LoginManager, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SECRET_KEY'] = os.getenv(key='TOKEN')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import User, Food


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_data = get_food_data(request.form.get('food_name'))
        if request.form.get('write_data'):
            if not current_user.is_authenticated:
                flash('You need authorization to do it.')
                return redirect(url_for('login'))
            else:
                data = request.form.get('write_data').split('-')
                name = data[0]
                calories = data[1]
                fat = data[2]
                new_food_item = Food(
                    name=name,
                    calories=calories,
                    fat=fat,
                    parent_user_id=current_user.id
                )
                db.session.add(new_food_item)
                db.session.commit()
                flash('Successfully added')
                return redirect(url_for('index'))
        if not new_data:
            name = None
            parsed_food_data = None
        else:
            name = new_data['text']
            try:
                parsed_food_data = new_data['parsed'][0]['food']['nutrients']
            except IndexError:
                flash('Wrong food name!')
                return redirect(url_for('index'))
            else:
                return render_template('index.html', name=name, food=parsed_food_data, current_user=current_user)
    return render_template('index.html', current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('This email does not exist. Please try again')
            return redirect(url_for('login'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Your password is incorrect. Please try again')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        user = User.query.filter_by(email=email).first()
        if not user:
            hashed_pass = generate_password_hash(password)
            new_user = User(email=email,
                            password=hashed_pass,
                            name=name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        else:
            flash('Such user already exists. Log in!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/food-list')
def show_food():
    food = Food.query.filter_by(parent_user_id=current_user.id).all()
    return render_template('food.html', food=food)


if __name__ == '__main__':
    app.run()
