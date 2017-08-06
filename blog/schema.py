# -*- coding: utf-8 -*-

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from blog.models import User, Post, Comment


class UserType(SQLAlchemyObjectType):

    class Meta:
        model = User
        interfaces = (relay.Node, )


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
    user = graphene.Field(UserType, id=graphene.Int())
    post = graphene.Field(PostType, id=graphene.Int())

    all_posts = SQLAlchemyConnectionField(
        PostType, offset=graphene.Int(), order_by=graphene.String())
    latest_comments = SQLAlchemyConnectionField(CommentType)

    def resolve_user(self, args, context, info):
        user = UserType.get_query(context).first()
        return user

    def resolve_post(self, args, context, info):
        post = PostType.get_query(context).first()
        return post

    def resolve_all_posts(self, args, context, info):
        query = PostType.get_query(context)
        order_by = args.get('order_by')
        if not order_by:
            order_by = Post.created_at.desc()
        query = query.order_by(order_by)
        offset = args.get('offset')
        if offset:
            query = query.offset(offset)
        return query.all()

    def resolve_latest_comments(self, args, context, info):
        query = CommentType.get_query(context)
        query = query.order_by(Comment.created_at.desc()).limit(10)
        return query.all()


schema = graphene.Schema(
    query=Query, types=[UserType, PostType, CommentType])
