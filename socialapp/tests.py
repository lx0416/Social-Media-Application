from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from .model_factories import *
from .serializers import *
from .api import *

# API Tests
class APITest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()

    # test GetProfile API
    def test_profileDetailAPIReturnsSuccess(self):
        url = reverse('get_profile', kwargs={'user':'1'})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

    # test UserList API
    def test_userListAPIReturnsSuccess(self):
        url = reverse('user_list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
   
   # test EditProfile API
    def test_editProfileAPIReturnsSuccessOnPk(self):
        url = reverse('edit_profile_api', kwargs={'pk':'1'})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

    # test EditProfile API bad pk
    def test_editProfileAPIReturnsFailOnBadPk(self):
        bad_url = "/api/profile/a"
        response = self.client.get(bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    # test EditProfile API is successful
    def test_editProfileAPIReturnsSuccess(self):
        username = "testperson"
        bio = "testing"
        profile_pic = "profile_pictures/default.png"
        profile = UserProfile.objects.update(username=username, bio=bio, profile_pic=profile_pic)
        data = {'bio': bio}
        response = self.client.get(reverse('edit_profile_api', kwargs={'pk':1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test AddPost API
    def test_addPostAPIReturnsSuccess(self):
        client = APIClient()
        client.force_authenticate(self.user)
        request_data = {
            "content": "content", 
            "datetime": "2022-03-13T15:54:00Z",
            "author": "1", 
        }
        response = self.client.post(reverse("post"), data=request_data)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
        client.logout()

    # test PostList API
    def test_postListAPIReturnsSuccess(self):
        url = reverse('posts')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

#######################################################################################################################################

# Views Tests
class ViewsTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    # test profile view
    def test_profileViewReturnsSuccess(self):
        url = "/login/?next=/profile/1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test profile view with login_required
    def test_profileViewRedirectReturnsSuccess(self):
        url = reverse('profile', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test register view
    def test_registerViewReturnsSuccess(self):
        url = "/register/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test login view
    def test_loginViewReturnsSuccess(self):
        url = "/login/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test logout view with login_required
    def test_logoutViewRedirectReturnsSuccess(self):
        url = "/logout/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test post list view
    def test_postListViewReturnsSuccess(self):
        url = "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test edit profile view with login_required
    def test_editProfileViewReturnsSuccess(self):
        url = reverse('edit_profile', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test add friends view
    def test_profileAddFViewReturnsSuccess(self):
        url = "/login/?next=/profile/1/friends/add"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test add friends view with login_required
    def test_profileAddFViewRedirectReturnsSuccess(self):
        url = reverse('add_friend', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test remove friends view
    def test_profileRemoveFViewReturnsSuccess(self):
        url = "/login/?next=/profile/1/friends/remove"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test remove friends view with login_required
    def test_profileRemoveFViewRedirectReturnsSuccess(self):
        url = reverse('remove_friend', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test search view
    def test_searchViewReturnsSuccess(self):
        url = "/login/?next=/search"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test search view with login_required
    def test_searchViewRedirectReturnsSuccess(self):
        url = reverse('user_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test friend list view
    def test_friendListViewReturnsSuccess(self):
        url = "/login/?next=/profile/1/friends"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test friend list view with login_required
    def test_friendListViewRedirectReturnsSuccess(self):
        url = reverse('friends_list', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test index view
    def test_indexViewReturnsSuccess(self):
        url = "/login/?next=/index"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test index view with login_required
    def test_indexViewRedirectReturnsSuccess(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # test room view
    def test_roomViewReturnsSuccess(self):
        url = "/login/?next=/chat/lobby"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test room view with login_required
    def test_roomViewRedirectReturnsSuccess(self):
        url = reverse('room', kwargs={'room_name': 'lobby'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)