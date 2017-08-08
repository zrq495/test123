# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from graphql_relay import from_global_id, to_global_id

from blog.schema import schema


class TestViews(object):

    def test_user_query(self, db, user):
        g_id = to_global_id('UserType', user.id)
        query = '''
        query {
            user (id: "%s") {
                id
                username
            }
        }
        ''' % g_id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['user']['id'] == g_id

    def test_post_query(self, db, post):
        g_id = to_global_id('PostType', post.id)
        query = '''
        query {
            post (id: "%s") {
                id
                title
            }
        }
        ''' % g_id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['post']['id'] == g_id

    def test_all_posts_query(self, db, post):
        query = '''
        query {
            allPosts (orderBy: {field: CREATED_AT, direction: DESC}, offset: 0){
                edges {
                    node {
                        id
                        title
                        user {
                            id
                            username
                        }
                    }
                }
            }
        }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert result.data['allPosts']['edges'][0]['node']['id'] == to_global_id('PostType', post.id)
        assert result.data['allPosts']['edges'][0]['node']['user']['id'] == to_global_id('UserType', post.user.id)

    def test_latest_comments_query(self, db, comment):
        query = '''
        query {
            latestComments {
                edges {
                    node {
                        id
                        content
                        user {
                            id
                            username
                        }
                        post {
                            id
                            title
                        }
                    }
                }
            }
        }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert result.data['latestComments']['edges'][0]['node']['id'] == to_global_id('CommentType', comment.id)
        assert result.data['latestComments']['edges'][0]['node']['user']['id'] == to_global_id('UserType', comment.user.id)
        assert result.data['latestComments']['edges'][0]['node']['post']['id'] == to_global_id('PostType', comment.post.id)
