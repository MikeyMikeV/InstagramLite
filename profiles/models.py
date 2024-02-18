from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tag = models.CharField(max_length=128)
    bio = models.CharField(max_length=128, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics')
    country = models.CharField(max_length=128, null=True, blank=True)
    region = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    nationality = models.CharField(max_length=128, null=True, blank=True)
    def __str__(self):
        return f'Profile {self.user.username}'
