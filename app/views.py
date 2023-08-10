from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
        token['username'] = user.username
        # ...

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
@api_view(['GET'])
def get_routes(request):
    routes_list = [
        'token',
        'token/refresh'
    ]

    return Response(routes_list)


@api_view(['GET'])
def get_user_info(request, user_id):
    
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialized_user = UserSerializer(user)

    return Response(serialized_user.data)