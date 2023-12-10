from django.urls import path

from . import views

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    # Authentication
    path('login/', views.login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', views.token_blacklist, name='token_blacklist'),
    path('register/', views.register_view, name='register'),
    path('security_questions', views.get_all_security_questions, name='all_security_questions'),
    path('reset_password/get_user_questions/', views.get_user_questions, name='get_user_questions'),
    path('reset_password/verify_answers/', views.verify_answers, name='verify_answers'),
    path('reset_password/done/', views.reset_password, name='reset_password'),

    # User
    path('user/<int:user_id>/posts', views.list_user_posts, name='list_user_posts'),
    path('user/<int:user_id>/comments', views.list_user_comments, name='list_user_comments'),
    path('user/<int:user_id>/post-likes', views.list_user_post_likes, name='list_user_post_likes'),
    path('user/<int:user_id>/comment-likes', views.list_user_comment_likes, name='list_user_comment_likes'),

    # Profiles
    path('profiles/<int:user_id>', views.view_profile, name='view_profile'),
    path('profiles/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),

    # Posts
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>', views.view_post, name='view_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),

    # Comments
    path('comments/<int:comment_id>', views.view_comment, name='view_comment'),
    path('comments/create/', views.create_comment, name='create_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),

    # Follow
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),

    # Message
    # path('send_message/', views.send_message, name="send_message"),
 
]