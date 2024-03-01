from django.db import models
from app.models import User


class ChatRoom(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_rooms")
    created = models.DateField(auto_now_add=True, editable=False)
    is_private = models.BooleanField(default=False)
    admins = models.ManyToManyField(User, blank=True, related_name="admin_in_rooms")
    members = models.ManyToManyField(User, blank=True, related_name="member_in_rooms")
    join_requests = models.ManyToManyField(User, blank=True, related_name="room_join_requests")


    # Override the default save method to make the creator as admin and member on creation
    def save(self, *args, **kwargs):
        # First save the room (to provide fk for other objects)
        super().save(*args, **kwargs)
        
        # Make the creator as admin and member
        self.admins.add(self.creator)
        self.members.add(self.creator)
        
    def __str__(self):
        return f"{self.name}"
    
    def is_admin(self, user):
        return user in self.admins.all()
    
    def is_member(self, user):
        return user in self.members.all()
    
    
class Message(models.Model):
    room = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.CharField(max_length=1000)
    file = models.FileField(upload_to='chat/files/', null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}'s message in {self.room}"
    

class ChatChannelName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clientships')
    channel_name = models.CharField(max_length=1000)

    def __str__(self):
        return f"channel_name of {self.user} in chat application"