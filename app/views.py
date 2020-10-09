from django.shortcuts import render
from .models import Faqs
from django.urls import reverse, reverse_lazy
from adm import views as admin_views
from engineer import views as engineer_views
from usr import views as user_views

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
        return user_views.index(response)
    elif group.name=="engineer":
        return engineer_views.index(response)
    elif group.name=="admin":
        return admin_views.index(response)

def dashboard(response):
    return render(response, "app/dashboard.html")

def base_template(request):
    context={}
    if request.user.is_authenticated and not request.user.is_superuser:
        user_group = request.user.groups.all()[0].name
        if user_group == 'user':
            context = {'base_template_name': 'usr/usr_dash.html'}
        elif user_group == 'admin':
            context = {'base_template_name': 'adm/admin_sidenav.html'}
        elif user_group == 'engineer':
            context = {'base_template_name': 'engineer/eng_sidenav.html'}
    
    if request.user.is_authenticated and request.user.is_superuser:
        context = {'base_template_name': 'adm/admin_sidenav.html'}
    return context
