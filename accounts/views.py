from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from  django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm
from . models import Profile

# Create your views here.

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def update_profile(request, pk):
    template = 'profile_update.html'
    profile = get_object_or_404(Profile, pk = pk)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('/dashboard')

    context = {"form": form}
    return render(request, template, context)