from django.conf import settings
from django.db.utils import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .helpers import get_tokens_for_user, get_object_or_404
from .models import *
from .serializers import *

import environ
env = environ.Env()

# ====================== Authentication =============================

@api_view(["POST"])
def register_view(request):
    '''
    A view that registers new user using:
    "first_name", "last_name", "email" and "password" and "security question/s"
    '''
    # Validate user's info (not containing sequrity questions)
    info = request.data.get('info')
    serializered_user = UserSerializer(data=info)
    serializered_user.is_valid(raise_exception=True)

    # Validate sequrity Q&A
    answers = request.data.get('answers')
    serializered_answers = SecurityAnswerSerializer(data=answers, many=True)
    serializered_answers.is_valid(raise_exception=True)

    # Check if the user has selected the same questions twice
    questions = []
    for question in serializered_answers.validated_data:
        if question in questions:
            return Response({"message": "You can't select the same question twice"})
        questions.append(question)
    
    # Everything is ok and valid
    # Save the user
    user = serializered_user.save()

    # # Add user_id to every security answer
    for data in serializered_answers.validated_data:
        data['user'] = user

    # # Save the Sequrity Q&A
    serializered_answers.save()

    # Get tokens
    tokens = get_tokens_for_user(user)

    return Response(tokens, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_view(request):
    '''
    A view that login users using "email" and "password"
    '''
    # Check the provided fields
    if not ("email" in request.data and "password" in request.data):
        return Response(
            {"Email and Password are required."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Try getting the user
    try:
        user = User.objects.get(email=request.data["email"])
    except User.DoesNotExist:
        return Response(
            {"User with this email not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # Check the password
    password = request.data["password"]
    check = user.check_password(password)
    if not check:
        return Response({"Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Get tokens
    tokens = get_tokens_for_user(user)

    # Return the tokens
    return Response(tokens, status=status.HTTP_200_OK)


# Get all the available security questions
@api_view(["GET"])
def get_all_security_questions(request):
    questions = SecurityQuestion.objects.all()
    serializer = SecurityQuestionSerializer(questions, many=True)

    return Response({"questions": serializer.data})


@api_view(["POST"])
def get_user_questions(request):
    # Check if email is provided in the request
    if not (email := request.data.get('email')):
        return Response({"message":"Email's not provided."})
    
    # User existance
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User with this email was not found."})
    
    # Get the user's security questions
    questions = SecurityAnswer.objects.filter(user=user)
    question_ids = [question.question.id for question in questions]

    return Response({
        "email": email,
        "questions": question_ids
        })


@api_view(["POST"])
def verify_answers(request):
    # Check if email is provided in the request
    if not (email := request.data.get('email')):
        return Response({"message":"Email's not provided."})
    
    # Check if answers are provided in the request
    if not (recieved_answers := request.data.get('answers')):
        return Response({"message":"Answers are not provided."})
    
    # User existance
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User with this email was not found."})
    
    # Get the user's security questions
    questions = SecurityAnswer.objects.filter(user=user)
    right_answers = {str(question.question.id): question.answer.lower() for question in questions}

    if not recieved_answers == right_answers:
        return Response({"message": "Answers are wrong."})
    
    ...
    subject = "Reset Password"
    message = f"Hello, Click this link to reset your password"

    send_mail(
        subject,
        message,
        "homam.s11@gmail.com",
        ["sadegh_mosawi@yahoo.com"],
        fail_silently=False,
    )

    return Response({"message": "Reset-Link was sent via email."})


# @api_view(["POST"])
# def forgot_password(request):
    # # Check if email is provided in the request
    # if not (email := request.data.get('email')):
    #     return Response({"message":"Email's not provided."})
    
    # # User existance
    # try:
    #     user = User.objects.get(email=email)
    # except User.DoesNotExist:
    #     return Response({"message": "User with this email was not found."})
    
    # token = default_token_generator.make_token(user)
    # uid = urlsafe_base64_encode(force_bytes(user.pk))
    # reset_link = f"blublublu/reset-password/{uid}/{token}/"

    # subject = "Reset Password"
    # message = f"Hello, Click this link to reset your password"
    # message = f"Hello, Click this link to reset your password {reset_link}"

    # email = request.data.get('email')
    # send_mail(
    #     subject,
    #     message,
    #     settings.EMAIL_HOST_USER,
    #     [email],
    #     fail_silently=False,
    # )

    # return Response("pass")


# Logout
@api_view(["POST"])
def token_blacklist(request):
    '''
    A view that get a refresh token and blacklist it
    '''
    # Take the refresh token from user and blacklist it
    try:
        token = request.data["refresh"]
        token = RefreshToken(token)
        token.blacklist()
    except KeyError:
        return Response(
            {"refresh": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response({"message": "Token Blacklisted"})


# ====================== Profile =============================


@api_view(["GET"])
def view_profile(request, user_id):
    # Retrieve the User and associated Profile objects
    user = get_object_or_404(User, pk=user_id)

    # Serialize and return the Profile data
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_profile(request, user_id):
    user = request.user

    # Check if the user owns the profile
    if not user.id == user_id:
        return Response(
            {"message": "You can't edit other's profiles."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Retrieve the profile, edit and save it
    serializer = UserSerializer(user, request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        {"message": "Profile successfully updated.", "data": serializer.data}
    )


# ====================== Post =============================

@api_view(["GET"])
def view_post(request, post_id):
    # Retrieve the post, serialzer and return it
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(post)
    return Response({"data": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    # Confirm that the request is multipart/form-data
    if not "multipart/form-data" in request.content_type:
        return Response(
            {"Error": "request content-type must be multipart/form-data"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Confirm that the post is created for the authenticated user (not someone else)
    data = request.data.copy()
    data["user"] = request.user.id

    # Serialize the post details and save them
    serializer = PostSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"result": "Post is created.", "data": serializer.data})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_post(request, post_id):
    # Check for post existance
    post = get_object_or_404(Post, pk=post_id)

    # Get the user from request
    user = request.user

    # Check if the the user owns the post
    if not post in user.posts.all():
        return Response(
            {"message": "You can't edit other's posts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Save the edited post
    edited_post = PostSerializer(post, request.data, partial=True)
    edited_post.is_valid(raise_exception=True)
    edited_post.save()

    return Response({"message": "Post is edited.", "data": edited_post.data})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    # Check for post existance
    post = get_object_or_404(Post, pk=post_id)

    # Get the user from request
    user = request.user

    # Check if the the user owns the post
    if not post in user.posts.all():
        return Response(
            {"message": "You can't delete other's posts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Delete the post
    post.delete()
    return Response({"Post is deleted."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):

    # Get the post
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user has liked the post before
    try:
        PostLike.objects.create(user=request.user, post=post)
    except IntegrityError:
        return Response(
            {"error": "You've already liked this post"},
            status=status.HTTP_409_CONFLICT
        )

    return Response({"message": "Post liked successfully", "total_likes": post.number_of_likes()}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_user_posts(request, user_id):
    # Check user existance
    user = get_object_or_404(User, pk=user_id)
    # Get user's posts
    posts = user.posts.all()

    # Check if the user has any posts, and return them
    if posts:
        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data})
    else:
        return Response({"No posts for this User."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def list_user_post_likes(request, user_id):

    # Check user existance
    user = get_object_or_404(User, pk=user_id)

    # Get user's post_likes
    post_likes = user.post_likes.all()

    # Check if the user has any post_likes, and return them
    if post_likes:
        serializer = PostLikeSerializer(post_likes, many=True)
        return Response({"post_likes": serializer.data})
    else:
        return Response({'message': 'No post_likes for this User.'}, status=status.HTTP_404_NOT_FOUND)


# ====================== Comment =============================

@api_view(["GET"])
def view_comment(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)

    serializer = CommentSerializer(comment)

    return Response({"data": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request):

    # Confirm that the comment is created for the authenticated user (not someone else)
    data = request.data.copy()
    # request.data._mutable = True
    data["user"] = request.user.id

    serializer = CommentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"message": "Comment created.", "data": serializer.data})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):

    # Get the comment
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the the user owns the post
    if not comment in request.user.comments.all():
        return Response(
            {"message": "You can't edit other's comments."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = CommentSerializer(comment, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"message": "Comment is edited.", "data": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):

    # Get the comment
    comment = get_object_or_404(Comment, pk=comment_id)

    # # Check if the user has liked the comment before
    try:
        CommentLike.objects.create(user=request.user, comment=comment)
    except IntegrityError:
        return Response(
            {"error": "You've already liked this comment"},
            status=status.HTTP_409_CONFLICT
        )

    return Response(
        {
            "message": "Comment liked successfully",
            "total_likes": comment.number_of_likes()
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reply_comment(request, comment_id):

    # Check if the parent comment exists or return 404
    get_object_or_404(Comment, pk=comment_id)

    # Confirm that the the user and the parent comment
    request.data['user'] = request.user.id
    request.data['parent'] = comment_id

    # Create the reply
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"message": "Reply is submitted.", "data": serializer.data})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):

    # Get the comment
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the the user owns the comment
    if not comment in request.user.comments.all():
        return Response(
            {"message": "You can't delete other's comments."},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.delete()

    return Response({"message": "Comment is deleted."})


@api_view(["GET"])
def list_user_comments(request, user_id):

    # Check user existance
    user = get_object_or_404(User, pk=user_id)

    # Get user's comments
    comments = user.comments.all()

    # Check if the user has any comments, and return them
    if comments:
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})
    else:
        return Response({"message": "No comments for this User."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def list_user_comment_likes(request, user_id):

    # Check user existance
    user = get_object_or_404(User, pk=user_id)

    # Get user's post_likes
    comment_likes = user.comment_likes.all()

    # Check if the user has any comments, and return them
    if comment_likes:
        serializer = CommentLikeSerializer(comment_likes, many=True)
        return Response({"comment_likes": serializer.data})
    else:
        return Response({"error": "No comment_likes for this User."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow(request, user_id):

    user = request.user
    user_to_follow = get_object_or_404(User, pk=user_id)

    # Insure not following self
    if user == user_to_follow:
        return Response({"error": "You can't follow yourself."})

    # Insure not currently following the target
    try:
        Follow.objects.create(follower=user, following=user_to_follow)
    except IntegrityError:
        return Response(
            {"error": "You're already following this user"},
            status=status.HTTP_409_CONFLICT
        )
    
    # Successfull
    return Response(
        {"message": f"Successfully followed {user_to_follow.full_name()}"},
        status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow(request, user_id):

    user = request.user

    user_to_unfollow = get_object_or_404(User, pk=user_id)



    try:
        follow = Follow.objects.get(follower=user, following=user_to_unfollow)
        follow.delete()
    except Follow.DoesNotExist:
        return Response(
            {"error": "You're not currently following this user"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({"message": f"Successfully unfollowed {user_to_unfollow.full_name()}"})


# ======================= Message =================================

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def send_message(request):

#     data = request.data.copy()
#     data['sender'] = request.user.id

#     serializer = MessageSerializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response({"message": "Message was sent."})