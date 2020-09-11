from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms import ModelForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'