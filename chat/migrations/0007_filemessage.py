# Generated by Django 5.0.1 on 2024-02-25 09:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_message_chatroom_message_thread'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='chat/files/')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]