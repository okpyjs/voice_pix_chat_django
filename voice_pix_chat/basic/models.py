from django.db import models

# Create your models here.


class AutoDate:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Plan(models.Model, AutoDate):
    name = models.CharField(max_length=200, unique=True)
    price = models.IntegerField(default=0)  # plan price
    chat_history_limit = models.IntegerField(default=30)  # expired chat history after 30 days
    emoji_publish_limit = models.IntegerField(default=10)  # define emoji numbers that users can publish emoji
    image_publish_limit = models.IntegerField(default=10)  # define emoji numbers that users can publish emoji
    daily_image_create_limit = models.IntegerField(default=20)  # define image numbers that users can create by ai
    description = models.TextField(default="No Description")
    private_message = models.BooleanField(default=True)
    video_call = models.BooleanField(default=True)
    audio_call = models.BooleanField(default=True)
