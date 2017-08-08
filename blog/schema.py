# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from blog.models import User, Post, Comment


class UserType(SQLAlchemyObjectType):

    class Meta:
        model = User
        interfaces = (relay.Node, )

    username = graphene.String(description='The username of the user')


class OrderByDirection(graphene.Enum):
    ASC = 'asc'
    DESC = 'desc'


class PostTypeOrderField(graphene.Enum):
    CREATED_AT = 'created_at'


class PostTypeOrder(graphene.InputObjectType):
    field = PostTypeOrderField(required=True)
    direction = OrderByDirection(default_value='asc')


class PostType(SQLAlchemyObjectType):

    class Meta:
        model = Post
        interfaces = (relay.Node, )


class CommentType(SQLAlchemyObjectType):

    class Meta:
        model = Comment
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = relay.Node.Field(UserType)
    post = relay.Node.Field(PostType)

    all_posts = SQLAlchemyConnectionField(
        PostType,
        first=graphene.Int(default_value=3),
        offset=graphene.Int(default_value=0),
        order_by=PostTypeOrder())
    latest_comments = SQLAlchemyConnectionField(CommentType)

    def resolve_all_posts(self, args, context, info):
        query = PostType.get_query(context)
        order_by = args.get('order_by')
        if not order_by:
            order_by = Post.created_at.desc()
        else:
            order_by = getattr(getattr(Post, order_by['field']), order_by['direction'])()
        query = query.order_by(order_by)
        offset = args['offset']
        query = query.offset(offset)
        return query.all()

    def resolve_latest_comments(self, args, context, info):
        query = CommentType.get_query(context)
        query = query.order_by(Comment.created_at.desc()).limit(10)
        return query.all()


schema = graphene.Schema(
    query=Query, types=[UserType, PostType, CommentType])
