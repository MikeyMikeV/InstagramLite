from django.db import models
from profiles.models import Profile
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_author')
    content = models.ManyToManyField('PostAttachment')
    text = models.CharField(max_length=256)
    likes = models.ManyToManyField(Profile, related_name='likes',blank=True)
    shares = models.ManyToManyField(Profile, related_name='shares',blank=True)
    comments = models.ManyToManyField('Comment')
    timestamp = models.DateTimeField(auto_now_add = timezone.now)

class PostAttachment(models.Model):
    image = models.ImageField(upload_to='post_attachment/')

class Comment(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='author', null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null = True)
    text = models.TextField(max_length=256)
    likes = models.ManyToManyField(Profile,related_name='numOfLikes',blank=True)
    timestamp = models.DateTimeField(auto_now_add = timezone.now)


from django.dispatch import receiver
import os

@receiver(models.signals.post_delete, sender = PostAttachment)
def auto_delete_file_on_delete(sender, instance:PostAttachment, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        print(f'File \'{instance.image}\' is deleted')
        os.remove(instance.image.path)