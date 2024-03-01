# from django.test import SimpleTestCase
# from django.urls import reverse, resolve

# # Import views
# from rest_framework_simplejwt.views import TokenRefreshView
# from app.views import *


# # Inherit from SimpleTestCase whenever not interacting with database

# # ==================== Authentication-related urls ==========================

# class TestAuthenticationUrls(SimpleTestCase):

#     def test_login_url_is_resolves(self):

#         url = reverse('login')
        
#         self.assertEqual(resolve(url).func, login_view)


#     def test_token_refresh_url_is_resolves(self):

#         url = reverse('token_refresh')

#         self.assertEqual(resolve(url).func.view_class, TokenRefreshView)


#     def test_token_blacklist_url_is_resolves(self):

#         url = reverse('token_blacklist')

#         self.assertEqual(resolve(url).func, token_blacklist)


#     def test_register_url_is_resolves(self):

#         url = reverse('register')

#         self.assertEqual(resolve(url).func, register_view)


# # ==================== User-related urls ==========================

# class TestUserUrls(SimpleTestCase):

#     def test_list_user_posts_url_is_resolves(self):

#         url = reverse('list_user_posts', args=[1])

#         self.assertEqual(resolve(url).func, list_user_posts)


#     def test_list_user_comments_url_is_resolves(self):

#         url = reverse('list_user_comments', args=[1])

#         self.assertEqual(resolve(url).func, list_user_comments)


#     def test_list_user_post_likes_url_is_resolves(self):

#         url = reverse('list_user_post_likes', args=[1])

#         self.assertEqual(resolve(url).func, list_user_post_likes)


#     def test_list_user_comment_likes_url_is_resolves(self):

#         url = reverse('list_user_comment_likes', args=[1])

#         self.assertEqual(resolve(url).func, list_user_comment_likes)


# # ==================== Profile-related urls ==========================

# class TestProfileUrls(SimpleTestCase):

#     def test_view_profile_url_is_resolves(self):

#         url = reverse('view_profile', args=[1])
        
#         self.assertEqual(resolve(url).func, view_profile)


#     def test_edit_profile_url_is_resolves(self):

#         url = reverse('edit_profile', args=[1])
        
#         self.assertEqual(resolve(url).func, edit_profile)


# # ==================== Post-related urls ==========================

# class TestPostUrls(SimpleTestCase):

#     def test_create_post_url_is_resolves(self):

#         url = reverse('create_post')
        
#         self.assertEqual(resolve(url).func, create_post)


#     def test_view_post_url_is_resolves(self):

#         url = reverse('view_post', args=[1])
        
#         self.assertEqual(resolve(url).func, view_post)


#     def test_edit_post_url_is_resolves(self):

#         url = reverse('edit_post', args=[1])
        
#         self.assertEqual(resolve(url).func, edit_post)


#     def test_delete_post_url_is_resolves(self):

#         url = reverse('delete_post', args=[1])
        
#         self.assertEqual(resolve(url).func, delete_post)

#     def test_like_post_url_is_resolves(self):

#         url = reverse('like_post', args=[1])
        
#         self.assertEqual(resolve(url).func, like_post)


# # ==================== Comment-related urls ==========================

# class TestCommentUrls(SimpleTestCase):

#     def test_create_comment_url_is_resolves(self):

#         url = reverse('create_comment')
        
#         self.assertEqual(resolve(url).func, create_comment)


#     def test_view_comment_url_is_resolves(self):

#         url = reverse('view_comment', args=[1])
        
#         self.assertEqual(resolve(url).func, view_comment)


#     def test_edit_comment_url_is_resolves(self):

#         url = reverse('edit_comment', args=[1])
        
#         self.assertEqual(resolve(url).func, edit_comment)


#     def test_delete_comment_url_is_resolves(self):

#         url = reverse('delete_comment', args=[1])
        
#         self.assertEqual(resolve(url).func, delete_comment)


#     def test_like_comment_url_is_resolves(self):

#         url = reverse('like_comment', args=[1])
        
#         self.assertEqual(resolve(url).func, like_comment)


#     def test_reply_comment_url_is_resolves(self):

#         url = reverse('reply_comment', args=[1])
        
#         self.assertEqual(resolve(url).func, reply_comment)


# # ==================== Follow-related urls ==========================

# class TestFollowUrls(SimpleTestCase):

#     def test_follow_url_is_resolves(self):

#         url = reverse('follow', args=[1])
        
#         self.assertEqual(resolve(url).func, follow)


#     def test_unfollow_url_is_resolves(self):

#         url = reverse('unfollow', args=[1])
        
#         self.assertEqual(resolve(url).func, unfollow)