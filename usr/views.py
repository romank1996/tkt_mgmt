from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Tickets
from django.http import HttpResponseRedirect
# from django.urls import reverse 

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    return render(response, 'usr/dashboard.html',{})

@login_required(login_url='/login/')
def my_tickets(response):
    tickets = Tickets.objects.filter(user = response.user).all
    return render(response, 'usr/tickets.html',{'tickets':tickets})    

@login_required(login_url='/login/')
def file_a_ticket(response):
    if response.method == "POST":
        form = TicketForm(response.POST or None)
        if form.is_valid():
            tickets = form.save(commit=False)
            tickets.user = response.user
            tickets.save()
            return redirect('/dashboard/my_tickets/')
    else:
        form=TicketForm()
    args = {'form': form}

    return render(response, 'usr/file_a_ticket.html',args)