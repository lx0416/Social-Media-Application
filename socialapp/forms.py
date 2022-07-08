from django import forms
from .models import *
from django.contrib.auth.models import User

# Form for the underlying User table that Django authentication system provides
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# Form to support our AppUser Model
class UserBirthForm(forms.ModelForm):
    birthdate = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'DD/MM/YYYY',
        })
    )
    class Meta:
        model = AppUser
        fields = ('birthdate', )

# Form to support our UserPost Model
class PostForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '5',
            'placeholder': "What's on your mind?",
        })
    )
    class Meta:
        model = UserPost
        # fields only contains content here as the other fields are automated bts
        fields = ['content']