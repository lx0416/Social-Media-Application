from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy

from .models import *
from .forms import *

# view used for user logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')

# view used for user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'socialapp/login.html')

# view used for registration
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        birth_form = UserBirthForm(data=request.POST)

        if user_form.is_valid() and birth_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save() # for saving into django db
            profile = birth_form.save(commit=False)
            profile.user = user            
            profile.save() # for saving into sqlite db
            registered = True
        else:
            print(user_form.errors, birth_form.errors)
    else:
        user_form = UserForm()
        birth_form = UserBirthForm()

    return render(request, 'socialapp/register.html',
                  {'user_form': user_form,
                    'birth_form': birth_form,
                    'registered': registered})                    

# view used for public status posts (root)
class PostListView(ListView):
    def get(self, request, *args, **kwargs):
        # Uncomment below for filtering out friend's status posts
        # current_user = request.user
        # posts = UserPost.objects.filter(
        #     author__profile__friends__in = [current_user.id]) | UserPost.objects.filter(
        #     author__profile__user = current_user
        # ).order_by('-datetime')
        posts = UserPost.objects.all().order_by('-datetime')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'socialapp/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = UserPost.objects.all().order_by('-datetime')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'socialapp/post_list.html', context)

# view used for profile
class ProfileView(ListView):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = UserPost.objects.filter(author=user).order_by('-datetime')
        friends = profile.friends.all()

        if len(friends) == 0:
            is_friend = False

        for friend in friends:
            if friend == request.user:
                is_friend = True
                break
            else:
                is_friend = False
        no_of_friends = len(friends)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'no_of_friends': no_of_friends,
            'is_friend': is_friend,
        }

        return render(request, 'socialapp/profile.html', context)

# view used for creating user profile upon creating a new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# view used for saving the user profile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# view used for editing user's profile
class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['username', 'bio', 'profile_pic']
    template_name = 'socialapp/edit_profile.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

# view used for adding friends
class AddFriend(LoginRequiredMixin, ListView):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.friends.add(request.user)
        return redirect('profile', pk=profile.pk)

# view used for removing friends
class RemoveFriend(LoginRequiredMixin, ListView):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.friends.remove(request.user)
        return redirect('profile', pk=profile.pk)

# view used for searching for users
class UserSearchView(ListView):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__startswith=query)
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'socialapp/search.html', context)

# view used for viewing friends list
class FriendsListView(ListView):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        friends = profile.friends.all()

        context = {
            'profile': profile,
            'friends': friends,
        }

        return render(request, 'socialapp/friends_list.html', context)

# view used for creating and entering chat room
def index(request):
    return render(request, 'socialapp/index.html')

# view used for chat room messages
def room(request, room_name):
    if request.method == 'GET':
        profile = UserProfile.objects.get(pk=request.user)
        username = profile.user.username
    return render(request, 'socialapp/room.html', {'room_name': room_name, 'username': username })