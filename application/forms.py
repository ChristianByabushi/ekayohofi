# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    province = forms.CharField(max_length=50, help_text='Required')
    city = forms.CharField(max_length=50, help_text='Required')
    role = forms.CharField(max_length=50, help_text='Required')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1',
                  'password2', 'province', 'city', 'role')
