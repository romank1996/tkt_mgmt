from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(response):
    args = {}
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return render(response, 'login/', {})
    else:
        form=RegisterForm()
    args['form'] = form

    return render(response, "register/register.html", {'form':form})