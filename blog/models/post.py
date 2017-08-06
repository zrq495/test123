# -*- coding: utf-8 -*-

from blog.database import db

__all__ = [
    'Post',
    'Comment',
]


class Post(db.Model):

    __table_name__ = 'post'

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False, index=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.String(16), nullable=False, index=True, server_default=STATUS_DRAFT)
    published_at = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())

    comments = db.relationship(
        'Comment', lazy='dynamic',
        backref=db.backref('post'),
        primaryjoin='Comment.post_id==Post.id',
        foreign_keys='Comment.post_id')

    user = db.relationship(
        'User',
        primaryjoin='User.id==Post.user_id',
        foreign_keys='Post.user_id')


class Comment(db.Model):

    __tablename__ = 'comment'

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False, index=True)
    post_id = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.String(16), nullable=False, index=True, server_default=STATUS_DRAFT)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())

    user = db.relationship(
        'User',
        primaryjoin='User.id==Comment.user_id',
        foreign_keys='Comment.user_id')
