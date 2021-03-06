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

    def test_all_posts_query(self, db, comment):
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
                        comments (orderBy: {field: CREATED_AT, direction: DESC}, offset: 0) {
                            edges {
                                node {
                                    id
                                    content
                                }
                            }
                        }
                    }
                }
            }
        }
        '''
        result = schema.execute(query)
        assert not result.errors
        post = comment.post
        assert result.data['allPosts']['edges'][0]['node']['id'] == to_global_id('PostType', post.id)
        assert result.data['allPosts']['edges'][0]['node']['user']['id'] == to_global_id('UserType', post.user.id)
        assert result.data['allPosts']['edges'][0]['node']['comments']['edges'][0]['node']['id'] == to_global_id('CommentType', comment.id)

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

    def test_create_post_query(self, user):
        query = '''
        mutation createPost {
          createPost(input:{title: "mutation title", userId: %s, content:"mutation content"}) {
                ok
                post{
                    id
                    userId
                    title
                    content
                }
            }
        }
        ''' % user.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['createPost']['ok'] is True
        assert result.data['createPost']['post']['userId'] == user.id

    def test_create_comment_query(self, user, post):
        query = '''
        mutation mycreateComment{
          createComment(
            input: {
              userId: %s
              content: "mutation comment"
              postId: %s
            }
          ) {
            ok
            comment{
              userId
              postId
              content
            }
          }
        }
        ''' % (user.id, post.id)
        result = schema.execute(query)
        assert not result.errors
        assert result.data['createComment']['ok'] is True
        assert result.data['createComment']['comment']['userId'] == user.id
        assert result.data['createComment']['comment']['postId'] == post.id
