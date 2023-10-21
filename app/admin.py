from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(SecurityQuestion)
admin.site.register(SecurityAnswer)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)