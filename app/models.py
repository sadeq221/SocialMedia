from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    # Override the default save method in order to create a profile object whenever a user object is created.
    def save(self, *args, **kwargs):

        # Is the instance being created ?
        created = not self.pk

        # Save the instance
        super().save(*args, **kwargs)

        # Intilize a profile for the new user
        if created:
            Profile.objects.create(user=self)


    # Checks if the user is following the given user?
    def is_following(self, user):
        return self.following.filter(following=user).exists()
    

    # Checks if the user is followed by the given user?
    def is_followed_by(self, user):
        return self.followers.filter(follower=user).exists()
    

    def __str__(self):
        return f"{self.name}"

    
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user}"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="unique_followers")
        ]

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=500)
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user}. title: {self.title}"
    
    def number_of_likes(self):
        return len(self.likes.all())
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='childs', null=True, blank=True)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"
    
    def number_of_likes(self):
        return len(self.likes.all())
    

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_post_likers")
        ]

    def __str__(self):
        return f"{self.user} liked {self.post.title}"
    

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_comment_likers")
        ]

    def __str__(self):
        return f"{self.user} liked a comment on {self.comment.post.title}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)