import json
import base64
from django.core.files.base import File, ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import *
from chat.serializers import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_anonymous:

            # Get all chatrooms which user is member in (with all details like messages)
            chatrooms = await self.get_chatrooms()

            # Create group name
            self.room_group_names = [
                f"chat_{chatroom['name']}" for chatroom in chatrooms
            ]

            # Join room group
            for group in self.room_group_names:
                await self.channel_layer.group_add(group, self.channel_name)

            await self.accept()

            # Add user's channel_name to the database
            await self.add_channel_name_to_database()

            # Send initialing message to the front end to create chatrooms
            await self.send(
                text_data=json.dumps(
                    {
                        "initial": True,
                        "chatrooms": chatrooms,
                        "user": self.user.full_name(),
                    }
                )
            )
        else:
            await self.close()

    async def disconnect(self, close_code): ...

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.pop("type")
        room_name = data["room"]

        # Add the sender object to the message data
        data["sender"] = self.user

        # Send message to room group
        if message_type == "chat.message":
            # Save message to database
            if message:= await self.save_message_to_database(data):
                await self.channel_layer.group_send(
                    f"chat_{room_name}", {"type": message_type, "data": message}
                )
            else:
                # Let the sender know about the sending failure
                # Let the front add options like retry sending (or just delete the message from screen)
                pass
        # If type is "leave" or "kick out", send the message just to the related instance
        else:
            await self.channel_layer.send(
                self.channel_name, {"type": message_type, "data": data}
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event["data"]))

    # Leave the group
    async def chat_leave(self, event):

        # Get the room group name
        room_name = event["data"]["room_name"]
        room_group_name = f"chat_{room_name}"

        # Prepare message data to be sent
        data = {
            "room_name": room_name,
            "message": f"{self.user.full_name()} left.",
            "notify": True,
        }

        # Remove user's membership from chatroom (in database)
        if await self.remove_membership_from_database(self.user.id, room_name):

            # Notify other members in the same group
            await self.channel_layer.group_send(
                room_group_name, {"type": "chat.message", "data": data}
            )

            # Disconnect user out of room group
            await self.channel_layer.group_discard(room_group_name, self.channel_name)

            # Send a message to the user's browser to reload (to remove room from screen)
            await self.channel_layer.send(
                self.channel_name, {"type": "chat.message", "data": {"reload": True}}
            )

            # Delete user's channel_name from database
            await self.delete_channel_name_from_database(user_id=self.user.id)

    # Kick out a user
    async def chat_kick_out(self, event):
        # Get kicked user id
        user_id = event["data"]["user_id"]
        kicked_user = await self.get_channel_name_from_database(user_id)

        # Get the room group name
        room_name = event["data"]["room_name"]
        room_group_name = f"chat_{room_name}"

        # Remove user's membership from chatroom (in database)
        if await self.remove_membership_from_database(user_id, room_name):

            # Prepare message data to be sent
            data = {
                "room_name": room_name,
                "message": f"{kicked_user['full_name']} is kicked out.",
                "notify": True,
            }

            # Notify other members in the same group
            await self.channel_layer.group_send(
                room_group_name, {"type": "chat.message", "data": data}
            )

            # Disconnect user out of room group
            await self.channel_layer.group_discard(room_group_name, self.channel_name)

            kicked_channel_name = kicked_user["channel_name"]
            # Send a message to the kicked user's browser to reload (to remove room from screen)
            await self.channel_layer.send(
                kicked_channel_name, {"type": "chat.message", "data": {"reload": True}}
            )

            # Delete user's channel_name from database
            await self.delete_channel_name_from_database(user_id=user_id)

    # Add user's channel_name to database
    @database_sync_to_async
    def add_channel_name_to_database(self):
        client, created = ChatChannelName.objects.get_or_create(user=self.scope["user"])
        client.channel_name = self.channel_name
        client.save()

    # Get channel_name from databasee
    @database_sync_to_async
    def get_channel_name_from_database(self, user_id):
        client = ChatChannelName.objects.get(user=user_id)
        return {
            "full_name": client.user.full_name(),
            "channel_name": client.channel_name,
        }

    # Delete user's channel_name from database
    @database_sync_to_async
    def delete_channel_name_from_database(self, user_id=None):

        # Determine the user object
        if user_id == None:
            user_id = self.scope["user"].id

        # Delete the channel name object
        try:
            client = ChatChannelName.objects.get(user=user_id)
            client.delete()
        except:
            ...

    @database_sync_to_async
    def get_chatrooms(self):

        # Get all chatrooms that user is member in
        chatrooms = self.user.member_in_rooms.all()
        serializer = UserChatRoomSerializer(
            chatrooms, context={"user": self.user}, many=True
        )
        return serializer.data

    @database_sync_to_async
    def remove_membership_from_database(self, user_id, room_name):
        try:
            chatroom = ChatRoom.objects.get(name=room_name)
            chatroom.members.remove(user_id)
            chatroom.admins.remove(user_id)
            return True
        except:
            return False

    @database_sync_to_async
    def save_message_to_database(self, data):
        message_data = {
            "room": data["room"],
            "sender": data["sender"].id,
            "content": data["content"]
        }
        
        # Does the message has a file?
        if data['file_data']:
            # Get the file as string and convert it to bytes using base64
            binary_file = base64.b64decode(data["file_data"])
            # Convert bytes to file content
            file_content = ContentFile(binary_file)
            # Create a file object
            message_data['file'] = File(file=file_content, name=data["file_name"])

        try:
            serializer = ChatMessageSerializer(data=message_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except:
            return False
