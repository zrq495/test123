# -*- coding: utf-8 -*-

from blog.database import db


class User(db.Model):

    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), nullable=False, unique=True, index=True)
    nickname = db.Column(db.String(128))
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
