from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Tickets
from .forms import TicketForm

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    return render(response, 'adm/dashboard.html',{})

@login_required(login_url='/login/')
def tickets(response):
    tickets = Tickets.objects.all()
    return render(response, 'adm/admin_tickets.html',{'tickets':tickets})


@login_required(login_url='/login/')
def create_new_ticket(response):
    if response.method == "POST":
        form = TicketForm(response.POST or None)
        if form.is_valid():
            tickets = form.save(commit=False)
            tickets.user = response.user
            tickets.save()
            return redirect('/dashboard/tickets')
    else:
        form=TicketForm()
    args = {'form': form}

    return render(response, 'adm/create_new_ticket.html',args)