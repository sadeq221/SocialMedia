# Generated by Django 5.0.1 on 2024-02-05 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chatchannelname_delete_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chatroom',
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.CharField(default='hello', max_length=255),
            preserve_default=False,
        ),
    ]
