# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from factory import Sequence, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory

from blog.models import *  # noqa
from blog.database import db


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):

    class Meta:
        model = User

    id = Sequence(lambda n: n)
    username = LazyAttribute(lambda obj: 'username{0}'.format(obj.id))
    nickname = LazyAttribute(lambda obj: 'nickname{0}'.format(obj.id))


class PostFactory(BaseFactory):

    class Meta:
        model = Post

    id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    title = LazyAttribute(lambda obj: 'post title {0}'.format(obj.id))
    content = LazyAttribute(lambda obj: 'content {0}\n'.format(obj.id) * 10)


class CommentFactory(BaseFactory):

    class Meta:
        model = Comment

    id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
    content = LazyAttribute(lambda obj: 'content {0}\n'.format(obj.id) * 10)
