import os

class Config:
    SECRET_KEY = 'secret-key'
    # other configurations
    
    # Configuration for SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
