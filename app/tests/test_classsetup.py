# from django.test import TestCase, Client
# from django.core.files.uploadedfile import SimpleUploadedFile
# from rest_framework.test import APIClient
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from django.urls import reverse

# from ..models import *


# class TestPostViews(TestCase):

#     @classmethod
#     def setUpClass(cls):

#         cls.client = Client()
#         cls.api_client = APIClient()

#         # Intilize a user
#         cls.user = User.objects.create(first_name="sadeq", email="s@s.com")
#         cls.user.set_password("s")
#         cls.user.save()

#         alaki = len(cls.user.posts.all())

#         cls.bearer = f"Bearer {str(AccessToken().for_user(cls.user))}"

#     # # ==================== Create post =======================

#     def test_valid_create_post_without_image(self):
#         alaki = len(self.user.posts.all())

#         # Data to be sent in request
#         data = {"title": "Post is created using test", "body": "Post body"}

#         # Define url for creating a post for the user
#         url = reverse("create_post")

#         response = self.client.post(url, data, HTTP_AUTHORIZATION=self.bearer)
#         alaki = len(self.user.posts.all())

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
#         alaki = len(self.user.posts.all())

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
#         alaki = len(self.user.posts.all())

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