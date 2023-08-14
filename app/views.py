import jwt
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import environ
env = environ.Env()

from .models import *
from .serializers import *


# Customizing token claims
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
@api_view(['GET'])
def get_routes(request):
    routes_list = {
        'register': ['name', 'email', 'password'],
        'login': ['email', 'password'],
        'token/refresh': 'refresh token'
    }

    return Response(routes_list)


class RegisterView(APIView):
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print(serializer.data)
        access_payload = {
            'user_id': serializer.data['id'],
            'name': serializer.data['name'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }
        access_token = jwt.encode(access_payload, env("JWT_SECRET"), 'HS256')

        refresh_payload = {
            'user_id': serializer.data['id'],
            'name': serializer.data['name'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=10)
        }
        refresh_token = jwt.encode(refresh_payload, env("JWT_SECRET"), 'HS256')

        tokens = {
            "refresh": refresh_token,
            "access": access_token
        }

        return Response(tokens, status=status.HTTP_201_CREATED)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):

    user = request.user

    posts = user.posts.all()

    if posts:
        code = status.HTTP_200_OK
    else:
        code = status.HTTP_204_NO_CONTENT

    serializer = PostSerializer(posts, many=True)

    return Response({"posts": serializer.data}, status=code)