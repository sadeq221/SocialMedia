# Generated by Django 5.0.1 on 2024-02-02 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='chatroom',
            field=models.CharField(max_length=255),
        ),
    ]