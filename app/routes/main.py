from flask import render_template
from app.forms.auth import LoginForm
from app import app

@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)
