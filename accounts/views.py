from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from  django.contrib.auth.forms import UserCreationForm

from .forms import ProfileForm, SignUpForm
from . models import Profile

# Create your views here.

# class based view for signup form
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# function based view used to accomodate contact_no in sign up form
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.contact_no = form.cleaned_data.get('contact_no')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def update_profile(request, pk):
    template = 'profile_update.html'
    profile = get_object_or_404(Profile, pk = pk)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('/dashboard')

    context = {"form": form}
    return render(request, template, context)