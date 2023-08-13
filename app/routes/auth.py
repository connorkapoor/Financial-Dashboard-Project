from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.auth import LoginForm, RegistrationForm
from app.models.user import User
from app import app, db
from app import login

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))  
    form = LoginForm()
    if form.validate_on_submit():
        # Query the database for this user
        user = User.query.filter_by(username=form.username.data).first()
        # Check the password entered against the hash stored in the database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_view'))
        # Log in the user
        login_user(user)
        # Redirect to the main page
        return redirect(url_for('dashboard'))  # Update according to the defined endpoint in main.py
    else:
        return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))  # Update according to the defined endpoint in main.py

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, you may now login.')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')