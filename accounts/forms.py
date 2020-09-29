from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    contact_no = forms.CharField()

    class Meta:
        model = User
        fields = ('username','email', 'contact_no', 'password1', 'password2',)

class UserRegisterAdmin(UserCreationForm):
    contact_no = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'contact_no', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']