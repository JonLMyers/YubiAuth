from flask import import Blueprint, render_template

UI = Blueprint('ui', __name__)

@UI.route('/')
def home():
    render_template('index.html')
