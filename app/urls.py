from django.urls import path

from . import views, my_tokens

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [

    # User
    # renaming "token" to "login"
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', views.token_blacklist, name='token_blacklist'),
    path('register/', views.register_view, name='register'),

    # Profiles
    path('profiles/<int:user_id>', views.view_profile, name='view_profile'),
    path('profiles/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    # path('profiles/<int:user_id>/avatar/edit/', views.edit_avatar, name='edit_avatar'),

    # Posts
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>', views.view_post, name='view_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('posts/user/<int:user_id>', views.list_user_posts, name='list_user_posts'),


    
]