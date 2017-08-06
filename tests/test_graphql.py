# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from blog.schema import schema


class TestViews(object):

    def test_user_query(self, db, user):
        query = '''
        query {
            user (id: %s) {
                id
                username
            }
        }
        ''' % user.id
        result = schema.execute(query)
        assert result.data['user']['username'] == user.username

    def test_post_query(self, db, post):
        query = '''
        query {
            post (id: %s) {
                id
                title
            }
        }
        ''' % post.id
        result = schema.execute(query)
        assert result.data['post']['title'] == post.title

    def test_all_posts_query(self, db, post):
        query = '''
        query {
            allPosts {
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
        assert result.data['allPosts']['edges'][0]['node']['title'] == post.title
        assert result.data['allPosts']['edges'][0]['node']['user']['username'] == post.user.username

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
        assert result.data['latestComments']['edges'][0]['node']['content'] == comment.content
        assert result.data['latestComments']['edges'][0]['node']['user']['username'] == comment.user.username
        assert result.data['latestComments']['edges'][0]['node']['post']['title'] == comment.post.title
