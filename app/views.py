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
        return render(response, 'usr/dashboard.html', {})
    elif group.name=="engineer":
        return render(response, 'engineer/dashboard.html',{})
    elif group.name=="admin":
        return render(response, 'adm/dashboard.html', {})

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
    
    return context
