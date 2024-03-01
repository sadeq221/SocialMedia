# from django.test import TestCase, Client
# from django.core.files.uploadedfile import SimpleUploadedFile
# from rest_framework.test import APIClient
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from django.urls import reverse

# from ..models import *


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