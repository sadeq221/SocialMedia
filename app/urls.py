from django.urls import path

from . import views, my_tokens

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [
    path('', views.get_routes, name='get_routes'),

    # renaming "token" to "login"
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('register/', views.register_view, name='register'),
    path('profiles/<int:user_id>', views.view_profile, name='view_profile'),
    path('profiles/<int:user_id>/edit', views.edit_profile, name='edit_profile'),





    # path('posts/', views.get_posts, name='get_posts'),
]