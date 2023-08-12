from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.get_routes, name='get_routes'),

    path('register/', views.RegisterView.as_view(), name='register'),
    # renaming "token" to "login"
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('posts/', views.get_posts, name='get_posts'),
    


    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]