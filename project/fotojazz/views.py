from flask import Module
from flask import render_template

mod = Module(__name__, 'fotojazz')

@mod.route('/')
def home():
    return render_template('home.html')
