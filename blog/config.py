# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = bool(os.environ.get('DEBUG'))

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxxhard to guess string'
    SSL_DISABLE = False

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog.sqlite')
