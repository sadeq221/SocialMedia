# from django.test import TestCase, Client
# from django.core.files.uploadedfile import SimpleUploadedFile
# from rest_framework.test import APIClient
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from django.urls import reverse

# from ..models import *

# # # ===============================================================
# # # ==================== User-related Tests =======================
# # # ===============================================================


# class TestUserViews(TestCase):

#     def setUp(self):

#         self.client = Client()

#         # URLs
#         self.register_url = reverse("register")
#         self.login_url = reverse("login")
#         self.token_refresh_url = reverse("token_refresh")
#         self.token_blacklist_url = reverse("token_blacklist")

#         # Register cridentials
#         self.register_cridentials = {
#             "name": "register",
#             "email": "register@register.com",
#             "password": "register",
#         }

#         # Create a user (to test login)
#         self.user = User.objects.create(name="user", email="user@user.com")
#         self.user.set_password("user")
#         self.user.save()

#         # Login cridentials
#         self.login_cridentials = {"email": "user@user.com", "password": "user"}

#         self.refresh = RefreshToken.for_user(self.user)

#     #     # # ====================== Test Register  =========================

#     def test_valid_register(self):

#         # register a user
#         response = self.client.post(self.register_url, data=self.register_cridentials)

#         # 201 Created status code
#         self.assertEqual(response.status_code, 201)

#         # Both tokens returned
#         self.assertTrue("refresh" in response.json())
#         self.assertTrue("access" in response.json())

#     def test_invalid_register_email_exists(self):

#         # Lets set an email that already exists in the database
#         self.register_cridentials["email"] = "user@user.com"

#         # register a user with the existant email
#         response = self.client.post(self.register_url, data=self.register_cridentials)

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(
#             response.json(), {"email": ["user with this email already exists."]}
#         )

#     def test_invalid_register_missing_fields(self):

#         # Send the request with empty cridentials
#         response = self.client.post(self.register_url, data={})

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {
#                 "name": ["This field is required."],
#                 "email": ["This field is required."],
#                 "password": ["This field is required."],
#             },
#         )

#     # # ======================= Test Login  ===========================

#     def test_valid_login(self):

#         # Send the request with valid cridentials
#         response = self.client.post(self.login_url, data=self.login_cridentials)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Both tokens returned
#         self.assertTrue("refresh" in response.json())
#         self.assertTrue("access" in response.json())

#     def test_invalid_login_missing_fields(self):

#         # Send the request with empty cridentials
#         response = self.client.post(self.login_url, data={})

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(response.json(), ["Email and Password are required."])

#     def test_invalid_login_user_not_exist(self):

#         # Let's set an "email" that doesn't exist in database
#         self.login_cridentials["email"] = "jafar@jafar.com"

#         # send the request with non-existant email
#         response = self.client.post(self.login_url, data=self.login_cridentials)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right message returned
#         self.assertEqual(response.json(), ["User with this email not found"])

#     def test_invalid_login_wrong_password(self):

#         # Let's change the "password"
#         self.login_cridentials["password"] = "987654321"

#         # Send a request with wrong password
#         response = self.client.post(self.login_url, data=self.login_cridentials)

#         # 401 Bad request status code
#         self.assertEqual(response.status_code, 401)

#         # Right message returned
#         self.assertEqual(response.json(), ["Incorrect password"])

#     # ==================== Test Token Refresh =======================

#     def test_valid_token_refresh(self):

#         # Prepare the refresh token as Json (to be sent)
#         refresh = {"refresh": str(self.refresh)}

#         # Send the current refresh token in order to get new refresh and access tokens.
#         response = self.client.post(self.token_refresh_url, data=refresh)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Both tokens returned
#         self.assertTrue("refresh" in response.json())
#         self.assertTrue("access" in response.json())

#     # Test when not providing "refresh token" field
#     def test_invalid_token_refresh_missing_token_field(self):

#         # Send a request without a refresh token.
#         response = self.client.post(self.token_refresh_url, data={})

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(response.json(), {"refresh": ["This field is required."]})

#     # Test when sending empty "refresh token"
#     def test_invalid_token_refresh_empty_token_field(self):

#         # Send a request with an empty refresh token.
#         response = self.client.post(self.token_refresh_url, data={"refresh": ""})

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(response.json(), {"refresh": ["This field may not be blank."]})

#     # Test when sending empty "refresh token"
#     def test_invalid_token_refresh_invalid_or_expired_token(self):

#         # Send a request with a wrong (same as expired) refresh token.
#         response = self.client.post(
#             self.token_refresh_url, data={"refresh": "ufhdfkfjdfj"}
#         )

#         # 401 Unauthorized status code
#         self.assertEqual(response.status_code, 401)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {"detail": "Token is invalid or expired", "code": "token_not_valid"},
#         )

#     # Test when sending a blacklisted "refresh token" to "token/refresh/"
#     def test_invalid_token_refresh_blacklisted(self):

#         # Blacklist the refresh token
#         self.refresh.blacklist()

#         # Prepare the refresh token as Json (to be sent)
#         refresh = {"refresh": str(self.refresh)}

#         # Let's send the blacklisted refresh token
#         response = self.client.post(self.token_refresh_url, data=refresh)

#         # 401 Unauthorized status code
#         self.assertEqual(response.status_code, 401)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {"detail": "Token is blacklisted", "code": "token_not_valid"},
#         )

#     # ==================== Test Token blacklist =====================

#     def test_valid_token_blacklist(self):

#         # Prepare the refresh token as Json (to be sent)
#         refresh = {"refresh": str(self.refresh)}

#         # Send the current refresh token in order to blacklist it.
#         response = self.client.post(self.token_blacklist_url, data=refresh)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Right message returned
#         self.assertEqual(response.json(), ["Token Blacklisted"])

#     def test_invalid_token_blacklist_missing_token_field(self):

#         # Send a request without a refresh token.
#         response = self.client.post(self.token_blacklist_url, data={})

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(response.json(), {"refresh": ["This field is required."]})


# # ===============================================================
# # ==================== Profile-related Tests ====================
# # ===============================================================


# class TestProfileViews(TestCase):

#     def setUp(self):

#         self.client = Client()
#         self.api_client = APIClient()

#         self.user = User.objects.create(name="Sadeq", email="s@s.com")
#         self.user.set_password("s")
#         self.user.save()

#         self.cridentials = {"email": self.user.email, "password": "s"}

#         self.profile = self.user.profile

#         self.bearer = f"Bearer {str(AccessToken().for_user(self.user))}"

#     # ==================== view profile ====================

#     def test_valid_view_profile(self):

#         # Send a request with existant user id
#         response = self.client.get(reverse("view_profile", args=[self.user.id]))

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Right response message
#         self.assertEqual(
#             response.json(),
#             {
#                 "user": self.profile.user.id,
#                 "avatar": self.profile.avatar,
#                 "bio": self.profile.bio,
#                 "birth_date": self.profile.birth_date,
#             },
#         )

#     def test_invalid_view_profile_user_not_exist(self):

#         # Send a request with not-existant user id
#         response = self.client.get(reverse("view_profile", args=[self.user.id + 1]))

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "User not found"})

#     # ==================== edit profile ====================

#     def test_valid_edit_profile(self):

#         # Open an image to set as avatar for profile
#         avatar_image = open("app/tests/files/image.JPG", "rb")

#         # Data to be sent in request
#         data = {"bio": "edited using test", "avatar": avatar_image}

#         # Define url for editing current user's profile
#         url = reverse("edit_profile", args=[self.user.id])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # Reassign self.profile in order to get the new version of it containing the avatar
#         self.profile = Profile.objects.get(user=self.user)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Right message returned
#         self.assertEqual(
#             response.data,
#             {
#                 "message": "Profile successfully updated.",
#                 "data": {
#                     "user": self.profile.user.id,
#                     "avatar": self.profile.avatar.url,
#                     "bio": self.profile.bio,
#                     "birth_date": self.profile.birth_date,
#                 },
#             },
#         )

#     # When user doesn't own the profile
#     def test_invalid_edit_profile_User_not_own_the_profile(self):

#         # Open an image to set as avatar for profile
#         avatar_image = open("app/tests/files/image.JPG", "rb")

#         # Data to be sent in request
#         data = {"bio": "edited using test", "avatar": avatar_image}

#         # Define url for editing [someone else's] profile
#         url = reverse("edit_profile", args=[self.user.id + 1])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 403 Forbidden status code
#         self.assertEqual(response.status_code, 403)

#         # Right message returned
#         self.assertEqual(response.data, {"message": "You can't edit other's profiles."})


# # # # ===============================================================
# # # # ==================== Post-related Tests =======================
# # # # ===============================================================


# class TestPostViews(TestCase):

#     def setUp(self):

#         self.client = Client()
#         self.api_client = APIClient()

#         # Intilize a user
#         self.user = User.objects.create(first_name="sadeq", email="s@s.com")
#         self.user.set_password("s")
#         self.user.save()

#         self.bearer = f"Bearer {str(AccessToken().for_user(self.user))}"

#     # # ==================== Create post =======================

#     def test_valid_create_post_without_image(self):

#         # Data to be sent in request
#         data = {"title": "Post is created using test", "body": "Post body"}

#         # Define url for creating a post for the user
#         url = reverse("create_post")

#         response = self.client.post(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # Get post details
#         post = self.user.posts.last()

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {
#                 "result": "Post is created.",
#                 "data": {
#                     "id": post.id,
#                     "title": post.title,
#                     "body": post.body,
#                     "image": post.image or None,
#                     "created": post.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": post.last_edited,
#                     "user": self.user.id,
#                 },
#             },
#         )

#     def test_valid_create_post_with_image(self):

#         # Open an image to set for the post
#         image = open("app/tests/files/image.JPG", "rb")

#         # Create a django file instance
#         uploaded_file = SimpleUploadedFile(
#             name="image.jpg", content=image.read(), content_type="image/jpeg"
#         )

#         # Data to be sent in request
#         data = {
#             "title": "Post is created using test",
#             "body": "Post body",
#             "image": uploaded_file,
#         }

#         # Define url for creating a post for the user
#         url = reverse("create_post")

#         response = self.client.post(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # Get post details
#         post = self.user.posts.last()

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {
#                 "result": "Post is created.",
#                 "data": {
#                     "id": post.id,
#                     "title": post.title,
#                     "body": post.body,
#                     "image": post.image.url,
#                     "created": post.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": post.last_edited,
#                     "user": self.user.id,
#                 },
#             },
#         )

#     def test_invalid_create_post_not_multipart_content_type(self):

#         # Define url for creating a post for the user
#         url = reverse("create_post")

#         # Data to be sent in request
#         data = {"title": "Post is created using test", "body": "Post body"}

#         # Send a request with wrong content_type
#         response = self.client.post(
#             url, data, content_type="text/plain", HTTP_AUTHORIZATION=self.bearer
#         )

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {"Error": "request content-type must be multipart/form-data"},
#         )

#     def test_invalid_create_post_missing_fields(self):

#         # Define url for creating a post for the user
#         url = reverse("create_post")

#         # Send a request with empty data
#         response = self.client.post(url, data={}, HTTP_AUTHORIZATION=self.bearer)

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {"title": ["This field is required."], "body": ["This field is required."]},
#         )

#     # ---------------- view post ------------------------------------

#     def test_valid_view_post(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Send a request with existant post id
#         response = self.client.get(reverse("view_post", args=[post.id]))

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # We need to check whether the post has image or not
#         # This is important before asserting the right data
#         try:
#             post_image = post.image.url
#         except ValueError:
#             post_image = None

#         # Right response message
#         self.assertEqual(
#             response.json(),
#             {
#                 "data": {
#                     "id": post.id,
#                     "title": post.title,
#                     "body": post.body,
#                     "image": post_image,
#                     "created": post.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": post.last_edited,
#                     "user": post.user.id,
#                 }
#             },
#         )

#     def test_invalid_view_post_not_exist(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Send a request with not-existant post id
#         response = self.client.get(reverse("view_post", args=[post.id + 1]))

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "Post not found"})

#     # ---------------------- edit post -----------------------

#     def test_valid_edit_post(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Open an image to set as image for the post
#         image = open("app/tests/files/image.JPG", "rb")

#         # Data to be sent in request
#         data = {"title": "edited using test", "body": "post body", "image": image}

#         # Define url for editing the created post
#         url = reverse("edit_post", args=[post.id])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Retrieve the post from database to get the updated info
#         post = Post.objects.filter(user=self.user).last()

#         # Right response message
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Post is edited.",
#                 "data": {
#                     "id": post.id,
#                     "title": post.title,
#                     "body": post.body,
#                     "image": post.image.url,
#                     "created": post.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": post.last_edited.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "user": post.user.id,
#                 },
#             },
#         )

#     def test_valid_edit_post_changing_user_has_no_effect(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Create new user
#         new_user = User.objects.create(name="hellofff", email="fffff")

#         # Data to be sent in request (trying to change the user of the post)
#         data = {"user": new_user.id, "title": "edited using test", "body": "post body"}

#         # Define url for editing the created post
#         url = reverse("edit_post", args=[post.id])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Retrieve the post from database to get the updated info
#         post = Post.objects.filter(user=self.user).last()

#         # Right response message
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Post is edited.",
#                 "data": {
#                     "id": post.id,
#                     "title": post.title,
#                     "body": post.body,
#                     "image": post.image or None,
#                     "created": post.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": post.last_edited.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     # User of the post is not changed (still self.user not changed to new_user)
#                     "user": self.user.id,
#                 },
#             },
#         )

#     def test_invalid_edit_post_not_found(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Data to be sent in request
#         data = {"title": "edited using test", "body": "post body"}

#         # Define url for editing non-existant post
#         url = reverse("edit_post", args=[post.id + 1])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "Post not found"})

#     # When user doesn't own the post
#     def test_invalid_edit_post_not_own_the_post(self):

#         # Create a user (other than self.user)
#         new_user = User.objects.create(name="Hello", email="h@h.com")

#         # Create a post for our new user
#         post = Post.objects.create(user=new_user)

#         # Data to be sent in request
#         data = {"title": "edited using test", "body": "post body"}

#         # Define url for editing current post
#         url = reverse("edit_post", args=[post.id])

#         # Send the request (with self.user's token (not the owner))
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 403 Forbidden status code
#         self.assertEqual(response.status_code, 403)

#         # Right response message
#         self.assertEqual(response.json(), {"message": "You can't edit other's posts."})

#     # ========================= Delete Post =============================

#     def test_valid_delete_post(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Define url for deleting existant post
#         url = reverse("delete_post", args=[post.id])

#         # Send deletion request and get the response
#         response = self.api_client.delete(url, HTTP_AUTHORIZATION=self.bearer)

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right response message
#         self.assertEqual(response.json(), ["Post is deleted."])

#     def test_invalid_delete_post_not_found(self):

#         # Create a post
#         post = Post.objects.create(user=self.user)

#         # Define url for deleting non-existant post
#         url = reverse("delete_post", args=[post.id + 1])

#         # Send deletion request and get the response
#         response = self.api_client.delete(url, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "Post not found"})

#     def test_invalid_delete_post_not_own_the_post(self):

#         # Create a user (other than self.user)
#         new_user = User.objects.create(name="Hello", email="h@h.com")

#         # Create a post for our new user
#         post = Post.objects.create(user=new_user)

#         # Define url for editing current post
#         url = reverse("delete_post", args=[post.id])

#         # Send the request (with self.user's token (not the owner))
#         response = self.api_client.delete(url, HTTP_AUTHORIZATION=self.bearer)

#         # 403 Forbidden status code
#         self.assertEqual(response.status_code, 403)

#         # Right response message
#         self.assertEqual(
#             response.json(), {"message": "You can't delete other's posts."}
#         )

#     #     # ====================== like a Post ==============================

#     def test_valid_like_post(self):

#         # Create a post
#         post = Post.objects.create(user=self.user, title="title", body="body")

#         # Define the like post url
#         url = reverse("like_post", args=[post.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 201 created status code
#         self.assertEqual(response.status_code, 201)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Post liked successfully",
#                 "total_likes": post.number_of_likes()
#             }
#         )

#     def test_invalid_like_post_not_found(self):

#         # Define url for non-existant post
#         url = reverse("like_post", args=[2])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": "Post not found"})

#     def test_invalid_like_post_already_liked(self):

#         # Create a post
#         post = Post.objects.create(user=self.user, title="title", body="body")

#         # Like the post
#         PostLike.objects.create(user=self.user, post=post)

#         # Define url for liking the already-liked post
#         url = reverse("like_post", args=[post.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 409 Conflict status code
#         self.assertEqual(response.status_code, 409)

#         # Right returned message
#         self.assertEqual(response.json(), {"error": "You've already liked this post"})

#     # ====================== List User Posts ===========================

#     def test_valid_list_user_posts(self):

#         # Create some posts
#         post1 = Post.objects.create(user=self.user)
#         post2 = Post.objects.create(user=self.user)

#         # Url for listing self.user's posts
#         url = reverse(f"list_user_posts", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {
#                 "posts": [
#                     {
#                         "id": post1.id,
#                         "title": post1.title,
#                         "body": post1.body,
#                         "image": post1.image or None,
#                         "created": post1.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                         "last_edited": post1.last_edited,
#                         "user": post1.user.id,
#                     },
#                     {
#                         "id": post2.id,
#                         "title": post2.title,
#                         "body": post2.body,
#                         "image": post2.image or None,
#                         "created": post2.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                         "last_edited": post2.last_edited,
#                         "user": post2.user.id,
#                     },
#                 ]
#             },
#         )

#     def test_invalid_list_user_posts_user_not_found(self):

#         # Url for listing posts of non-existant user
#         url = reverse(f"list_user_posts", args=[self.user.id + 1])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": "User not found"})

#     def test_invalid_list_user_posts_no_posts(self):

#         # Url for listing self.user's posts
#         url = reverse(f"list_user_posts", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), ["No posts for this User."])

#     # ====================== List User post likes ===========================

#     def test_valid_list_user_post_likes(self):

#         # Create two posts to like them
#         post1 = Post.objects.create(user=self.user)
#         post2 = Post.objects.create(user=self.user)

#         # Like the two created posts
#         like1 = PostLike.objects.create(user=self.user, post=post1)
#         like2 = PostLike.objects.create(user=self.user, post=post2)

#         # Url for listing self.user's post likes
#         url = reverse(f"list_user_post_likes", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {
#                 "post_likes": [
#                     {
#                         "id": like1.id,
#                         "user": like1.user.id,
#                         "post": like1.post.id,
#                         "created": like1.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     },
#                     {
#                         "id": like2.id,
#                         "user": like2.user.id,
#                         "post": like2.post.id,
#                         "created": like2.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     },
#                 ]
#             },
#         )

#     def test_invalid_list_user_post_likes_user_not_found(self):

#         # Url for listing post_likes of non-existant user
#         url = reverse(f"list_user_post_likes", args=[self.user.id + 1])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": "User not found"})

#     def test_invalid_list_user_post_likes_no_post_likes(self):

#         # Url for listing self.user's post_likes (which are none)
#         url = reverse(f"list_user_post_likes", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"message": "No post_likes for this User."})


# # # ===============================================================
# # # ==================== Comment-related Tests =======================
# # # ===============================================================


# class TestCommentViews(TestCase):

#     def setUp(self):

#         self.maxDiff = None

#         self.api_client = APIClient()

#         # Intilize a user
#         self.user = User.objects.create(name="sadeq", email="s@s.com")
#         self.user.set_password("s")
#         self.user.save()

#         self.post = Post.objects.create(
#             user=self.user, title="post title", body="post body"
#         )

#         self.comment = Comment.objects.create(
#             user=self.user, post=self.post, content="self.commet content"
#         )

#         self.bearer = f"Bearer {str(AccessToken().for_user(self.user))}"

#     # ================== Create Comment ==================
#     def test_valid_create_comment(self):

#         # Data to be sent in request
#         data = {"post": self.post.id, "content": "hello"}

#         # Define url for creating a comment for the user
#         url = reverse("create_comment")

#         response = self.api_client.post(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # Get comment details
#         comment = self.user.comments.last()

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Comment created.",
#                 "data": {
#                     "id": comment.id,
#                     "content": comment.content,
#                     "created": comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": comment.last_edited,
#                     "user": comment.user.id,
#                     "post": comment.post.id,
#                     "parent": comment.parent,
#                 },
#             },
#         )

#     def test_invalid_create_comment_missing_fields(self):

#         # Define url for creating a comment for the user
#         url = reverse("create_comment")

#         # Send the request with empty data
#         response = self.api_client.post(url, data={}, HTTP_AUTHORIZATION=self.bearer)

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {
#                 "post": ["This field is required."],
#                 "content": ["This field is required."],
#             },
#         )

#     # ================== View Comment ==================
#     def test_valid_view_comment(self):

#         # Send a request with existant comment id
#         response = self.api_client.get(reverse("view_comment", args=[self.comment.id]))

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right message returned
#         self.assertEqual(
#             response.json(),
#             {
#                 "data": {
#                     "id": self.comment.id,
#                     "content": self.comment.content,
#                     "created": self.comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": self.comment.last_edited,
#                     "user": self.comment.user.id,
#                     "post": self.comment.post.id,
#                     "parent": self.comment.parent,
#                 }
#             },
#         )

#     def test_invalid_view_comment_not_exist(self):

#         # Send a request with not-existant comment id
#         response = self.client.get(reverse("view_comment", args=[self.comment.id + 1]))

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "Comment not found"})

#     # ---------------------- edit comment -----------------------

#     def test_valid_edit_comment(self):

#         # Data to be sent in request
#         data = {
#             "content": "edited using test",
#         }

#         # Define url for editing the self.comment
#         url = reverse("edit_comment", args=[self.comment.id])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Retrieve the post from database to get the updated info
#         self.comment = Comment.objects.filter(user=self.user).last()

#         # Right response message
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Comment is edited.",
#                 "data": {
#                     "id": self.comment.id,
#                     "content": self.comment.content,
#                     "created": self.comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": self.comment.last_edited.strftime(
#                         "%Y-%m-%dT%H:%M:%S.%fZ"
#                     ),
#                     "user": self.comment.user.id,
#                     "post": self.comment.post.id,
#                     "parent": self.comment.parent,
#                 },
#             },
#         )

#     def test_valid_edit_comment_changing_user_and_post_has_no_effect(self):

#         new_user = User.objects.create(name="hellofff", email="fffff")

#         new_post = Post.objects.create(user=new_user, title="hekkkkk", body="dfdffdf")

#         # Data to be sent in request (trying to change the user and the post of the comment)
#         data = {
#             "user": new_user.id,
#             "post": new_post.id,
#             "content": "edited using test",
#         }

#         # Define url for editing the self.comment
#         url = reverse("edit_comment", args=[self.comment.id])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 200 OK status code
#         self.assertEqual(response.status_code, 200)

#         # Retrieve the post from database to get the updated info
#         self.comment = Comment.objects.filter(user=self.user).last()

#         # Right response message
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Comment is edited.",
#                 "data": {
#                     "id": self.comment.id,
#                     "content": self.comment.content,
#                     "created": self.comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     "last_edited": self.comment.last_edited.strftime(
#                         "%Y-%m-%dT%H:%M:%S.%fZ"
#                     ),
#                     "parent": self.comment.parent,
#                     # User and Post are not changed for the comment
#                     "user": self.comment.user.id,
#                     "post": self.comment.post.id,
#                 },
#             },
#         )

#     def test_invalid_edit_post_not_found(self):

#         # Data to be sent in request
#         data = {
#             "content": "edited using test",
#         }

#         # Define url for editing non-existant comment
#         url = reverse("edit_comment", args=[self.comment.id + 1])

#         # Send the data and get the response
#         response = self.api_client.patch(url, data, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "Comment not found"})

#     # When user doesn't own the comment
#     def test_invalid_edit_comment_not_own_the_comment(self):

#         # Create a user (other than self.user)
#         new_user = User.objects.create(name="Hello", email="h@h.com")

#         # Create a post for our new user
#         comment = Comment.objects.create(
#             user=new_user, post=self.post, content="comment for new user"
#         )

#         # Data to be sent in request
#         data = {"content": "edited using test"}

#         # Define url for editing current self.comment (which is not owend by self.user)
#         url = reverse("edit_comment", args=[comment.id])

#         # Send the data and get the response
#         response = self.api_client.patch(
#             url,
#             data,
#             # This bearer is for self.user
#             HTTP_AUTHORIZATION=self.bearer,
#         )

#         # 403 Forbidden status code
#         self.assertEqual(response.status_code, 403)

#         # Right response message
#         self.assertEqual(
#             response.json(), {"message": "You can't edit other's comments."}
#         )

#     # ========================= Delete Comment =============================
#     def test_valid_delete_comment(self):

#         # Define url for deleting existant comment
#         url = reverse("delete_comment", args=[self.comment.id])

#         # Send deletion request and get the response
#         response = self.api_client.delete(url, HTTP_AUTHORIZATION=self.bearer)

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right response message
#         self.assertEqual(response.json(), {"message": "Comment is deleted."})

#     def test_invalid_delete_comment_not_found(self):

#         # Define url for deleting non-existant comment
#         url = reverse("delete_comment", args=[self.comment.id + 1])

#         # Send deletion request and get the response
#         response = self.api_client.delete(url, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right response message
#         self.assertEqual(response.json(), {"detail": "Comment not found"})

#     def test_invalid_delete_comment_not_own_the_comment(self):

#         # Create a user (other than self.user)
#         new_user = User.objects.create(name="Hello", email="h@h.com")

#         # Create a post for our new user
#         comment = Comment.objects.create(
#             user=new_user, post=self.post, content="comment for new user"
#         )

#         # Define url for editing current comment
#         url = reverse("delete_comment", args=[comment.id])

#         # Send deletion request and get the response
#         response = self.api_client.delete(
#             url,
#             # This bearer is for self.user
#             HTTP_AUTHORIZATION=self.bearer,
#         )

#         # 403 Forbidden status code
#         self.assertEqual(response.status_code, 403)

#         # Right response message
#         self.assertEqual(
#             response.json(), {"message": "You can't delete other's comments."}
#         )

#     # ====================== like a comment ==============================

#     def test_valid_like_comment(self):

#         # Define the like comment url
#         url = reverse("like_comment", args=[self.comment.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 201 created status code
#         self.assertEqual(response.status_code, 201)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "Comment liked successfully",
#                 "total_likes": len(self.user.comment_likes.all()),
#             },
#         )

#     def test_invalid_like_comment_not_found(self):

#         # Define url for non-existant comment
#         url = reverse("like_comment", args=[2])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": "Comment not found"})

#     def test_invalid_like_comment_already_liked(self):

#         # Like the comment
#         CommentLike.objects.create(user=self.user, comment=self.comment)

#         # Define url for liking the already-liked comment
#         url = reverse("like_comment", args=[self.comment.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 409 Conflict status code
#         self.assertEqual(response.status_code, 409)

#         # Right returned message
#         self.assertEqual(
#             response.json(), {"error": "You've already liked this comment"}
#         )

#     # ====================== List User comments ===========================

#     def test_valid_list_user_comments(self):

#         # Create one more comment for self.user (in addition to self.comment)
#         comment = Comment.objects.create(
#             user=self.user, post=self.post, content="comment content"
#         )

#         # Url for listing self.user's comments
#         url = reverse(f"list_user_comments", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {
#                 "comments": [
#                     {
#                         "id": self.comment.id,
#                         "content": self.comment.content,
#                         "created": self.comment.created.strftime(
#                             "%Y-%m-%dT%H:%M:%S.%fZ"
#                         ),
#                         "last_edited": self.comment.last_edited,
#                         "parent": self.comment.parent,
#                         "user": self.comment.user.id,
#                         "post": self.comment.post.id,
#                     },
#                     {
#                         "id": comment.id,
#                         "content": comment.content,
#                         "created": comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                         "last_edited": comment.last_edited,
#                         "parent": comment.parent,
#                         "user": comment.user.id,
#                         "post": comment.post.id,
#                     },
#                 ]
#             },
#         )

#     def test_invalid_list_user_comments_user_not_found(self):

#         # Url for listing comments of non-existant user
#         url = reverse(f"list_user_comments", args=[self.user.id + 1])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": "User not found"})

#     def test_invalid_list_user_comments_no_comments(self):

#         # Craete new user with no comments
#         new_user = User.objects.create(name="dfjdfd", email="dkfkdfkd")

#         # Url for listing new_user's comments (which are none)
#         url = reverse(f"list_user_comments", args=[new_user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"message": "No comments for this User."})

#     # ====================== List User comment likes ===========================

#     def test_valid_list_user_comment_likes(self):

#         # Create one more comment for self.user (in addition to self.comment)
#         comment = Comment.objects.create(
#             user=self.user, post=self.post, content="comment content"
#         )

#         # Like the two comments (self.comment and comment created above)
#         like1 = CommentLike.objects.create(user=self.user, comment=self.comment)
#         like2 = CommentLike.objects.create(user=self.user, comment=comment)

#         # Url for listing self.user's comment likes
#         url = reverse(f"list_user_comment_likes", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 200 Ok status code
#         self.assertEqual(response.status_code, 200)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {
#                 "comment_likes": [
#                     {
#                         "id": like1.id,
#                         "user": like1.user.id,
#                         "comment": like1.comment.id,
#                         "created": like1.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     },
#                     {
#                         "id": like2.id,
#                         "user": like2.user.id,
#                         "comment": like2.comment.id,
#                         "created": like2.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#                     },
#                 ]
#             },
#         )

#     def test_invalid_list_user_comment_likes_user_not_found(self):

#         # Url for listing comment_likes of non-existant user
#         url = reverse(f"list_user_comment_likes", args=[self.user.id + 1])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": "User not found"})

#     def test_invalid_list_user_comment_likes_no_comment_likes(self):

#         # Url for listing self.user's comment_likes (which are none)
#         url = reverse(f"list_user_comment_likes", args=[self.user.id])

#         # Send the request
#         response = self.api_client.get(url)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"error": "No comment_likes for this User."})


# # # ===============================================================
# # # =================== Follow-related Tests =====================
# # # ===============================================================
# class TestFollowViews(TestCase):

#     def setUp(self):

#         self.api_client = APIClient()

#         self.follower = User.objects.create(name="follower", email="follower")
#         self.following = User.objects.create(name="following", email="following")

#         self.bearer = f"Bearer {str(AccessToken().for_user(self.follower))}"

#     # # =================== follow =====================

#     def test_valid_follow(self):

#         # Define url for follow view
#         url = reverse("follow", args=[self.following.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 201 Created status code
#         self.assertEqual(response.status_code, 201)

#         # Right returned message
#         self.assertEqual(
#             response.json(), {"message": f"Successfully followed {self.following.name}"}
#         )

#     def test_invalid_follow_user_not_found(self):

#         # Define url for following non-existant user
#         url = reverse("follow", args=[self.following.id + 1])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": f"User not found"})

#     def test_invalid_follow_user_already_followed(self):

#         # Create a follow object
#         Follow.objects.create(follower=self.follower, following=self.following)

#         # Define url for following an already-followed user
#         url = reverse("follow", args=[self.following.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 409 Conflict status code
#         self.assertEqual(response.status_code, 409)

#         # Right returned message
#         self.assertEqual(
#             response.json(), {"error": "You're already following this user"}
#         )

#     # # =================== unfollow =====================

#     def test_valid_unfollow(self):

#         # Let's create a follow object to be able to unfollow
#         Follow.objects.create(follower=self.follower, following=self.following)

#         # Define url for unfollow view
#         url = reverse("unfollow", args=[self.following.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 200 Created status code
#         self.assertEqual(response.status_code, 200)

#         # Right returned message
#         self.assertEqual(
#             response.json(),
#             {"message": f"Successfully unfollowed {self.following.name}"},
#         )

#     def test_invalid_unfollow_user_not_found(self):

#         # Define url for unfollowing non-existant user
#         url = reverse("unfollow", args=[self.following.id + 1])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 404 Not found status code
#         self.assertEqual(response.status_code, 404)

#         # Right returned message
#         self.assertEqual(response.json(), {"detail": f"User not found"})

#     def test_invalid_unfollow_user_not_currently_followed(self):

#         # Define url for unfollowing a user that is not currently followed
#         url = reverse("unfollow", args=[self.following.id])

#         response = self.api_client.post(url, HTTP_AUTHORIZATION=self.bearer)

#         # 400 Bad request status code
#         self.assertEqual(response.status_code, 400)

#         # Right returned message
#         self.assertEqual(
#             response.json(), {"error": "You're not currently following this user"}
#         )
