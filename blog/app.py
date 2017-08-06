# -*- coding: utf-8 -*-

from flask import Flask
from werkzeug.utils import find_modules, import_string

from flask_graphql import GraphQLView


from blog.database import db
from blog.config import Config
from blog.schema import schema


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    for name in find_modules('blog.views'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql', schema=schema, graphiql=True))



def register_extensions(app):
    db.init_app(app)
    db.app = app
