import os

from flask import current_app as app
from flask import Module
from flask import render_template
from flask import send_from_directory


mod = Module(__name__, 'fotojazz')

@mod.route('/')
def home():
    return render_template('home.html')

@mod.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')
