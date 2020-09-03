from django.shortcuts import render
from .models import Faqs

def index(response):
    return render(response, "app/base.html", {})

def faq(response):
    faqs = Faqs.objects.all()
    return render(response,"app/faq.html", {"list":faqs} )

def home(response):
    return render(response, "app/home.html", {})

def signedin(response):
    group = response.user.groups.filter(user=response.user)[0]
    if group.name=="user":
        return render(response, 'usr/dashboard.html', {"uname": response.user.username})
    elif group.name=="engineer":
        return render(response, 'engineer/dashboard.html',{"uname": response.user.username})
    elif group.name=="admin":
        return render(response, 'adm/dashboard.html', {"uname": response.user.username})