from rest_framework import serializers
from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('name',)
        
        
# Purpose: list slight-info rooms (ex: as search results)
class ListChatRoomSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    
    def get_members_count(self, obj):
        return obj.members.count()
    
    class Meta:
        model = ChatRoom
        fields = ('name', 'members_count')
        
# Purpose: get user's rooms info (including messages)
class UserChatRoomSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    
    def get_is_admin(self, obj):
        user = self.context.get('user')
        return obj.is_admin(user)
    
    def get_messages(self, obj):
        # Get all message objects based on the room name
        messages_objs = Message.objects.filter(room=obj.name)
        # Serialize messages
        message_serializer = ChatMessageSerializer(messages_objs, many=True)
        return message_serializer.data
    
    class Meta:
        model = ChatRoom
        fields = ('name', 'is_admin', 'messages')
        
        
# Purpose: get messages to show in rooms
class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    # Override the default data_time field for datetime() special representation
    date_time = serializers.SerializerMethodField()
    
    def get_date_time(self, obj):
        return f"{obj.date_time.date()} {obj.date_time.time().strftime('%H:%M:%S')}"
    
    def get_sender_name(self, obj):
        return obj.sender.full_name()
    
    class Meta:
        model = Message
        fields = ('room', 'sender', 'sender_name', 'content', 'file', 'date_time')