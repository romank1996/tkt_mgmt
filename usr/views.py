from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    group = response.user.groups.filter(user=response.user)[0]
    if group.name=="user":
        return render(response, 'usr/dashboard.html',{})
    elif group.name=="engineer":
        return HttpResponseRedirect(reverse('engineer'))
    elif group.name=="admin":
        return HttpResponseRedirect(reverse('adm'))

    return render(response, 'usr/dashboard.html',{})