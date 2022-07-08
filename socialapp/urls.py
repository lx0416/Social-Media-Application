from django.urls import path
from . import views
from . import api
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('profile/<int:pk>', login_required(login_url='login')(views.ProfileView.as_view()), name="profile"),
    path('profile/edit/<int:pk>', login_required(login_url='login')(views.EditProfileView.as_view()), name="edit_profile"),
    path('profile/<int:pk>/friends/add', login_required(login_url='login')(views.AddFriend.as_view()), name='add_friend'),
    path('profile/<int:pk>/friends/remove', login_required(login_url='login')(views.RemoveFriend.as_view()), name='remove_friend'),
    path('search/', login_required(login_url='login')(views.UserSearchView.as_view()), name='user_search'),
    path('profile/<int:pk>/friends', login_required(login_url='login')(views.FriendsListView.as_view()), name='friends_list'),
    path('index/', login_required(login_url='login')(views.index), name='index'),
    path('chat/<str:room_name>/', login_required(login_url='login')(views.room), name='room'),
    path('api/profile/<int:user>', api.GetProfile.as_view(), name='get_profile'),
    path('api/profile/edit/<int:pk>', api.EditProfile.as_view(), name='edit_profile_api'),
    path('api/profiles', api.UserList.as_view(), name='user_list'),
    path('api/post', api.AddPost.as_view(), name='post'),
    path('api/posts', api.PostList.as_view(), name='posts'),
]