# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from blog.app import create_app


@pytest.fixture
def app():
    _app = create_app()
    with _app.test_request_context():
        yield _app
