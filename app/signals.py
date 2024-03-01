from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from .models import User


# Signals
successful_login = Signal()


# Handlers
@receiver(successful_login)
def notify_login(sender, **kwargs):
    print(f"{sender.full_name()} logged in.")

