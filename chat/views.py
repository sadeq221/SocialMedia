from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom
from .serializers import ChatRoomSerializer, ListChatRoomSerializer
from app.helpers import get_object_or_404


def index(request):
    return render(request, "chat/index.html", {})


def chatrooms(request):

    return render(request, "chat/chatrooms.html")


# API
class ListAllRooms(APIView):
    def get(self, request):
        chatrooms = ChatRoom.objects.all()
        serializer = ListChatRoomSerializer(chatrooms, many=True)

        return Response(serializer.data)


class CreateRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data)
        # Convert the recieved chatroom name to lowercase
        serializer.initial_data['name'] = serializer.initial_data['name'].lower()
        serializer.is_valid(raise_exception=True)

        # Define the current user as the chat room creator
        serializer.validated_data['creator'] = request.user
        serializer.save()

        return Response("Chat room was created sucessfuly.")
    

class RoomInfo(APIView):
    def get(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)
        

class AddRoomMember(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())

        # Confirm the current user is Admin
        if not room.is_admin(request.user):
            return Response("Only admins can add members.")
        
        # Add each member of the list to the room
        members = request.data['members']
        for member in members:
            try:
                room.members.add(member)
            except:
                pass

        return Response('Members were added.')
    

class JoinRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())

        if room.is_member(request.user):
            return Response("User's already a member.")
        
        elif room.is_private:
            room.join_requests.add(request.user)
            return Response("A join request was sent.")
        
        else:
            room.members.add(request.user)
            return Response("User is added successfuly.")
        

class LeaveRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())

        if not room.is_member(request.user):
            return Response("User's not a member.")
        
        else:
            room.admins.remove(request.user)
            room.members.remove(request.user)
            return Response("User is removed successfuly.")
        

class MakeRoomAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())
        # Get the user to be admin
        new_admin = request.data['member']

        # Confirm the current user is Admin
        if not room.is_admin(request.user):
            return Response("Only admins can make admins.")
        
        # Confirm his membership
        elif not room.is_member(new_admin):
            return Response("User's not a member.")
        
        # Confirm not being an admin already
        elif room.is_admin(new_admin):
            return Response("User's already an Admin.")
        
        # Make admin
        else:
            room.admins.add(new_admin)
            return Response('New admin is added.')


class AcceptJoinRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())

        accepted_member = request.data['member']

        room.members.add(accepted_member)
        room.join_requests.remove(accepted_member)

        return Response("Join request is accepted.")


class RejectJoinRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        room = get_object_or_404(ChatRoom, room_name.lower())

        room.join_requests.remove(request.data['member'])

        return Response("Join request is rejected.")