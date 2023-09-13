from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import *


class TestUserModel(TestCase):

    def setUp(self):

        self.user1 = User.objects.create(name="sadeq",email="s@s.com")
        self.user2 = User.objects.create(name="Ali",email="a@a.com")

        # user1 started following user2
        Follow.objects.create(follower=self.user1, following=self.user2)


    # Test for profile creation whenever new user is created
    def test_user_has_profile(self):

        # Try to get the user's profile
        try:
            profile = self.user1.profile
        except User.profile.RelatedObjectDoesNotExist:
            profile = False
            
        self.assertTrue(profile)


    def test_is_following(self):

        self.assertTrue(self.user1.is_following(self.user2))
        self.assertFalse(self.user2.is_following(self.user1))


    def test_is_followed_by(self):

        self.assertTrue(self.user2.is_followed_by(self.user1))
        self.assertFalse(self.user1.is_followed_by(self.user2))


class TestFollowModel(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(name="sadeq",email="s@s.com")
        self.user2 = User.objects.create(name="Ali",email="a@a.com")
        # user1 started following user2
        Follow.objects.create(follower=self.user1, following=self.user2)

    
    def test_unique_follower(self):

        # Try to make user1 following user2 again
        try:
            follow_again = Follow.objects.create(follower=self.user1, following=self.user2)
        except IntegrityError:
            follow_again = False

        self.assertFalse(follow_again)


class TestPostModel(TestCase):

    def setUp(self):

        self.user1 = User.objects.create(name="user1", email="u1@u.com")
        self.user2 = User.objects.create(name="user2", email="u2@u.com")
        self.post = Post.objects.create(user=self.user1, title="post", body="post")


    def test_number_of_likes(self):
        
        # Both users like self.post
        PostLike.objects.create(user=self.user1, post=self.post)
        PostLike.objects.create(user=self.user2, post=self.post)

        self.assertEqual(self.post.number_of_likes(), 2)


class TestCommentModel(TestCase):

    def setUp(self):

        self.user1 = User.objects.create(name="user1", email="u1@u.com")
        self.user2 = User.objects.create(name="user2", email="u2@u.com")
        self.post = Post.objects.create(user=self.user1, title="post", body="post")
        self.comment = Comment.objects.create(user=self.user1, post=self.post, content="comment")


    def test_number_of_likes(self):
        
        # Both users like self.comment
        CommentLike.objects.create(user=self.user1, comment=self.comment)
        CommentLike.objects.create(user=self.user2, comment=self.comment)

        self.assertEqual(self.comment.number_of_likes(), 2)


class TestPostLikeModel(TestCase):

    def setUp(self):

        self.user = User.objects.create(name="sadeq",email="s@s.com")
        self.post = Post.objects.create(user=self.user, title="post", body="post")
        # user1 likes self.post
        PostLike.objects.create(user=self.user, post=self.post)

    
    def test_unique_post_likers(self):

        # Try to make user1 liking self.post again
        try:
            like_again = PostLike.objects.create(user=self.user, post=self.post)
        except IntegrityError:
            like_again = False

        self.assertFalse(like_again)


class TestCommentLikeModel(TestCase):

    def setUp(self):

        self.user = User.objects.create(name="sadeq",email="s@s.com")
        self.post = Post.objects.create(user=self.user, title="post", body="post")
        self.comment = Comment.objects.create(user=self.user, post=self.post, content="content")

        # user1 likes self.comment
        CommentLike.objects.create(user=self.user, comment=self.comment)

    
    def test_unique_post_likers(self):

        # Try to make user1 liking self.comment again
        try:
            like_again = CommentLike.objects.create(user=self.user, comment=self.comment)
        except IntegrityError:
            like_again = False

        self.assertFalse(like_again)