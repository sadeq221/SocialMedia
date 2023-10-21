from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'avatar', 'bio', 'birth_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = "__all__"


class SecurityAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityAnswer
        fields = ["question", "answer"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def update(self, instance, validated_data):

        # Remove unpdatable fields (if they're provided)
        excluded_fields = ['user', 'created']
        for field in excluded_fields:
            validated_data.pop(field, None)
            
        # Call the parent class's update method to perform default update logic
        instance = super().update(instance, validated_data)

        # Update the 'last_updated' field to the current datetime.
        instance.last_edited = datetime.utcnow()
        
        instance.save()
        return instance
    

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):

        # Remove unpdatable fields (if they're provided)
        excluded_fields = ['user', 'post', 'created', 'parent']
        for field in excluded_fields:
            validated_data.pop(field, None)
            
        # Call the parent class's update method to perform default update logic
        instance = super().update(instance, validated_data)

        # Update the 'last_updated' field to the current datetime.
        instance.last_edited = datetime.utcnow()
        
        instance.save()
        return instance


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields= "__all__"

#     def create(self, validated_data):
#         if validated_data['sender'] == validated_data['receiver']:
#             raise ValidationError("User can't send message to himself.", code='invalid')