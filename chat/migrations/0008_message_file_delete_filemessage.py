# Generated by Django 5.0.1 on 2024-02-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_filemessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='chat/files/'),
        ),
        migrations.DeleteModel(
            name='FileMessage',
        ),
    ]
