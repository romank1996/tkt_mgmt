from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group

# Create your views here.
def register(response):
    args = {}
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            return render(response, '/login', {})
    else:
        form=RegisterForm()
    args['form'] = form

    return render(response, "register/register.html", {'form':form})