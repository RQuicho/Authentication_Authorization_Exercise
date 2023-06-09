from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from config import *
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(name)

app.config.from_object("config")
toolbar = DebugToolbarExtension(app)

connect_db(app)

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
        new_user = User.register(username, pwd, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another username.')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id

        flash('Account created!', 'success')
        return redirect('/secret')


    
