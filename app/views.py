from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .my_tokens import get_tokens_for_user

import environ
env = environ.Env()

from .models import *
from .serializers import *


@api_view(['GET'])
def get_routes(request):
    routes_list = {
        'register': ['name', 'email', 'password'],
        'login': ['email', 'password'],
        'token/refresh': 'refresh token'
    }

    return Response(routes_list)


@api_view(['POST'])
def register_view(request):

    serializered_user = UserSerializer(data=request.data)
    serializered_user.is_valid(raise_exception=True)
    serializered_user.save()

    user = User.objects.get(id=serializered_user.data['id'])

    # Intilize a Profile for the new User
    Profile.objects.create(user=user)

    # Get tokens
    tokens = get_tokens_for_user(user)

    return Response(tokens, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def view_profile(request, user_id):

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except:
        return Response({"message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializered_prof = ProfileSerializer(profile)

    return Response(serializered_prof.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request, user_id):

    user = request.user

    if not user.id == user_id:
        return Response({"message": "You can't edit other's profiles."}, status=status.HTTP_401_UNAUTHORIZED)
        
    profile = Profile.objects.get(user=user)
    serializered_prof = ProfileSerializer(profile)

    if request.method == 'GET':
        return Response(serializered_prof.data)
    
    elif request.method == 'PUT':
        form = ProfileSerializer(serializered_prof, request.data) 

        form.is_valid(raise_exception=True)
        form.save()
        return Response({'message': 'profile Updated.'})




        
        



















# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_posts(request):

#     user = request.user

#     posts = user.posts.all()

#     if posts:
#         code = status.HTTP_200_OK
#     else:
#         code = status.HTTP_204_NO_CONTENT

#     serializer = PostSerializer(posts, many=True)

#     return Response({"posts": serializer.data}, status=code)