from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = models.User
        fields = ('email', 'password1', 'password2')