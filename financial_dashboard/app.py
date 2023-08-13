from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# configure Flask-Login
login = LoginManager(app)
login.login_view = 'login'

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize database
from models import db
db.init_app(app)
migrate = Migrate(app, db)


@login.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    from models import User
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        #query the database for this user
        user = User.query.filter_by(username=form.username.data).first()
        #check the password entered against the hash stored in the database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #log in the user
        login_user(user)
        #redirect to the main page
        return redirect(url_for('main'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/')
def main():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)

