from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('chatrooms', views.chatrooms, name="enter_room"),

    # API
    path('api/chatroom/list', views.ListAllRooms.as_view(), name='list_all_rooms'),
    path('api/chatroom/create/', views.CreateRoom.as_view(), name='create_room'),
    path('api/chatroom/<str:room_name>', views.RoomInfo.as_view(), name='room_info'),
    path('api/chatroom/<str:room_name>/join/', views.JoinRoom.as_view(), name='join_room'),
    path('api/chatroom/<str:room_name>/join_request/accept', views.AcceptJoinRequest.as_view(), name='accept_join_request'),
    path('api/chatroom/<str:room_name>/join_request/reject', views.RejectJoinRequest.as_view(), name='reject_join_request'),
    path('api/chatroom/<str:room_name>/leave/', views.LeaveRoom.as_view(), name='join_room'),
    path('api/chatroom/<str:room_name>/add_member/', views.AddRoomMember.as_view(), name='add_room_member'),
    path('api/chatroom/<str:room_name>/make_admin/', views.MakeRoomAdmin.as_view(), name='make_room_admin'),
]
