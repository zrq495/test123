# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from blog.app import create_app, db as _db

from factories import *  # noqa


@pytest.fixture
def app():
    _app = create_app()
    _app.config['DEBUG'] = True
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    with _app.test_request_context():
        yield _app


@pytest.fixture
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture
def user(db):
    u = UserFactory()
    db.session.commit()
    return u


@pytest.fixture
def post(db):
    p = PostFactory()
    db.session.commit()
    return p


@pytest.fixture
def comment(db):
    c = CommentFactory()
    db.session.commit()
    return c
