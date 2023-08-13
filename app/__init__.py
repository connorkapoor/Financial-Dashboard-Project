from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # Set the session lifetime here

db = SQLAlchemy(app)
Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login_view'

from app.routes import main, auth
from app.models import user

