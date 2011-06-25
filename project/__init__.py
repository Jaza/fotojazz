fotojazz_processes = {}

from flask import Flask
app = Flask(__name__)
app.config.from_object('project.settings')

from project.fotojazz.views import mod
app.register_module(mod)
