from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from config import *
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config.from_object("config")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def back_to_register():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def create_new_user():
    """Shows and handles form that creates a new user"""
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another username.')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id

        flash('Account created!', 'success')
        return redirect('/secret')

    return render_template('register.html', form=form)


@app.route('/secret')
def show_secret_page():
    """Shows secret page if user is logged in"""
    form = RegisterForm()
    return render_template('secret.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login existing user"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            session["user_id"] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    """Logout user and clear session"""
    form = LoginForm()
    if request.method == 'POST':
        session.pop('user_id')
        flash('Logged out!', 'info')
        return redirect('/')
    return render_template('logout.html', form=form)


    
