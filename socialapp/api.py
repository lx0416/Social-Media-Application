from django.views.generic.detail import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import mixins

# API for retrieving profile by id
class GetProfile(APIView):
    def get(self, request, user):
        profile = UserProfile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

# API for retrieving all users' information
class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        users = User.objects.all()
        return users

# API for editing profile
class EditProfile(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# API for posting status updates
class AddPost(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = UserPost.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# API for retrieving all status posts
class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        posts = UserPost.objects.all()
        return posts