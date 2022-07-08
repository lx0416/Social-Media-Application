from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model for birthdate field
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.CharField(max_length=10, null=False, blank=False)
    def __unicode__(self):
        return self.user.username

# Model for status posts
class UserPost(models.Model):
    content = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# Model for profile edit
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.png', blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')