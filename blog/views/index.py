# -*- coding: utf-8 -*-

from flask import Blueprint

from blog.models import User

bp = Blueprint('index', __name__)


@bp.route("/")
def index():
    return "Welcome !"


@bp.route("/hello")
def hello():
    return "Hello World!"
