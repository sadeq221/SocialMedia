# import json
# from django.test import TestCase
# from channels.testing import WebsocketCommunicator
# from channels.db import database_sync_to_async
# from social.asgi import channels_asgi_application
# from rest_framework_simplejwt.tokens import AccessToken
# from chat.models import User, ChatRoom
# from chat.serializers import UserChatRoomSerializer


# class TestChatConsumer(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create(email='e@e.com')
        
#         # Create some chatrooms and add the user
#         self.room1 = ChatRoom.objects.create(name='room1', creator=self.user)
#         self.room1.members.add(self.user)
#         self.room2 = ChatRoom.objects.create(name='room2', creator=self.user)
#         self.room2.members.add(self.user)
        
#         # Get the user's detailed chatrooms (including messages)
#         # the data that is sent to front-end
#         rooms_serializer = UserChatRoomSerializer(
#             self.user.member_in_rooms.all(),
#             context={"user": self.user},
#             many=True
#             )
#         self.detailed_rooms = rooms_serializer.data
        
#         # Create access token for the user
#         self.bearer = str(AccessToken.for_user(self.user))

#     # -----------------------------
#     # Test connect() method
#     # -----------------------------
#     async def test_successful_connect(self):
        
#         communicator = WebsocketCommunicator(
#             channels_asgi_application, f"ws/chatrooms/?token={self.bearer}"
#         )

#         connected, subprotocol = await communicator.connect()

#         self.assertTrue(connected)

#         await communicator.disconnect()
        
#     async def test_failed_connect_anonymous_user(self):
        
#         # Not providing token (leads to anonymous user)
#         communicator = WebsocketCommunicator(
#             channels_asgi_application, f"ws/chatrooms/"
#         )

#         connected, subprotocol = await communicator.connect()

#         self.assertFalse(connected)

#         await communicator.disconnect()
        
#     async def test_initial_message(self):
        
#         communicator = WebsocketCommunicator(
#             channels_asgi_application, f"ws/chatrooms/?token={self.bearer}"
#         )

#         connected, subprotocol = await communicator.connect()
#         self.assertTrue(connected)
        
#         message = await communicator.receive_from()
#         message = json.loads(message)
        
#         self.assertEqual(message, {
#             'initial': True,
#             'chatrooms': self.detailed_rooms,
#             'user': self.user.full_name()
#         })

#         await communicator.disconnect()
