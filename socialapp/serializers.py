from rest_framework import serializers
from . models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'profile_pic','friends']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['username','email','profile']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['content', 'datetime', 'author']