from rest_framework import serializers

from datetime import datetime

class Comment():
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


mycomment = Comment(email='h@h.com', content='hello everyone')
serializer = CommentSerializer(mycomment)

print(serializer.data)