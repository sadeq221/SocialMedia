import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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

        # Log the user in to get jwt tokens
        login_url = f"http://{request.headers['Host']}/api/login/"

        creditionals = {
            "email": request.data['email'],
            "password": request.data['password']
        }

        tokens = requests.post(login_url, json=creditionals).json()

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