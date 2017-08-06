# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import url_for


class TestViews(object):

    def test_app(self, app):
        assert app.name == 'blog.app'

    def test_index(self, app):
        with app.test_client() as c:
            res = c.get(url_for('index.index'))
            assert res.status_code == 200

    def test_hello(self, app):
        with app.test_client() as c:
            res = c.get(url_for('index.hello'))
            assert res.status_code == 200
            assert res.data == 'Hello World!'
