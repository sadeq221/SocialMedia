from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
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
    routes_list = [
        'register',
        'login',
        'token/refresh',
        'token/blacklist',
        'profiles/user_id',
        'profiles/user_id/edit/'
    ]

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


@api_view(['POST'])
def token_blacklist(request):

    token = request.data['refresh']
    token = RefreshToken(token)
    token.blacklist()

    return Response({"Token Blacklisted"})

    

# --------------------- profile ---------------------------------------------------------------------
@api_view(['GET'])
def view_profile(request, user_id):

    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except:
        return Response({"message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializered_prof = ProfileSerializer(profile)

    return Response(serializered_prof.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile(request, user_id):

    user = request.user

    if not user.id == user_id:
        return Response({"message": "You can't edit other's profiles."}, status=status.HTTP_401_UNAUTHORIZED)
        
    profile = user.profile

    updated_prof = ProfileSerializer(profile, request.data, partial=True) 
    updated_prof.is_valid(raise_exception=True)
    updated_prof.save()

    return Response({'message': 'profile Updated.'})


# ---------------------------------------------------------------------------------------------------------

# ------------------------ Post ---------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):

    serializer = PostSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"result":"Post is created.", "data":serializer.data})


@api_view(['GET'])
def view_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    serializer = PostSerializer(post)

    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    user = request.user

    # Check if the the user owns the post
    if not post in user.posts.all():
        return Response({"message": "You can't edit other's posts."}, status=status.HTTP_401_UNAUTHORIZED)
    
    edited_post = PostSerializer(post, request.data, partial=True)
    edited_post.is_valid(raise_exception=True)
    try:
        edited_post.save()
    except Exception as e:
        return Response({str(e)})
    
    return Response({"Post is edited."})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    user = request.user

    # Check if the the user owns the post
    if not post in user.posts.all():
        return Response({"message": "You can't delete other's posts."}, status=status.HTTP_401_UNAUTHORIZED)
    
    post.delete()

    return Response({"Post is deleted."})


@api_view(['GET'])
def list_user_posts(request, user_id):

    user = get_object_or_404(User, pk=user_id)
    posts = user.posts.all()

    if posts:
        serializer = PostSerializer(user.posts.all(), many=True)
        return Response(serializer.data)
    else:
        return Response({"No posts for this User."})

