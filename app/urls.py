from django.urls import path

from . import views, my_tokens

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.get_routes, name='get_routes'),

    # renaming "token" to "login"
    path('login/', my_tokens.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('register/', views.register_view, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profiles/<int:user_id>', views.view_profile, name='view_profile'),
    path('profiles/<int:user_id>/edit', views.edit_profile, name='edit_profile'),





    # path('posts/', views.get_posts, name='get_posts'),
]