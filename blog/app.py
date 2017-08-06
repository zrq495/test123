# -*- coding: utf-8 -*-

from flask import Flask
from werkzeug.utils import find_modules, import_string


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app):
    for name in find_modules('blog.views'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
