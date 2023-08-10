from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('user/<int:user_id>/', views.get_user_info, name='get_user_info'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]