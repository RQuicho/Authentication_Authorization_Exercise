from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from config import *
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config.from_object("config")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
# db.create_all()
# User.query.delete()
# Feedback.query.delete()


@app.route('/')
def back_to_register():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Shows and handles form that creates a new user"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another username.')
            return render_template('register.html', form=form)
        session['username'] = user.username

        flash('Account created!', 'success')
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login existing user"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    """Logout user and clear session"""
    form = LoginForm()
    if request.method == 'POST':
        session.pop('username')
        flash('Logged out!', 'info')
        return redirect('/login')
    return render_template('logout.html', form=form)


@app.route('/users/<username>')
def show_secret_page(username):
    """Shows feedback page if user is logged in"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=username).all()
    return render_template('user_details.html', user=user, feedback=feedback)


    
