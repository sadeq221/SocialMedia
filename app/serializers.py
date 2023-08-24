from datetime import datetime

from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
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
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True}
        }



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

        # extra_kwargs = {
        #     'user': {'read_only': True},
        #     'created': {'read_only': True}
        # }

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