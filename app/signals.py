# from django.dispatch import receiver
# from django.dispatch import Signal
# from django.db.models.signals import post_save
# from .models import User, Profile


# # Signals
# successful_login = Signal()


# # Handlers
# @receiver(successful_login)
# def notify_login(sender, user, **kwargs):
#     print(f"{user} logged in.")


# @receiver(post_save, sender=User)
# def create_profile_when_user_created(sender, instance, created, **kwargs):
    
#     if created:
#         Profile.objects.create(user=instance)

