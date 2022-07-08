import factory
from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    username = "test"
    email = "test@example.com"

    class Meta:
        model = User

class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    username = "admin"
    bio = "i like turtles"
    profile_pic = 'profile_pictures/default.png'

    class Meta:
        model = UserProfile

class PostFactory(factory.django.DjangoModelFactory):
    content = "Hello everyone"
    datetime = '2022-03-13T15:54:00Z'
    author = factory.SubFactory(User)

    class Meta:
        model = UserPost