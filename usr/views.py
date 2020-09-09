from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Tickets

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    return render(response, 'usr/dashboard.html',{})

@login_required(login_url='/login/')
def tickets(response):
    tickets = Tickets.objects.filter(user = response.user).all
    return render(response, 'usr/tickets.html',{'tickets':tickets})

@login_required(login_url='/login/')
def create_new_ticket(response):
    if response.method == "POST":
        form = TicketForm(response.POST or None)
        if form.is_valid():
            tickets = form.save(commit=False)
            tickets.user = response.user
            tickets.save()
            return render(response, 'usr/create_new_ticket.html', {})
    else:
        form=TicketForm()
    args = {'form': form}

    return render(response, 'usr/create_new_ticket.html',args)