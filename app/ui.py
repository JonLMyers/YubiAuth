from flask import import Blueprint, render_template

UI = Blueprint('ui', __name__)

@UI.route('/')
def home():
    render_template('index.html')

@UI.route('/login')
def login():
    render_template('login.html')

@UI.route('/authenticated')
def authenticated():
    render_template('authed.html')
