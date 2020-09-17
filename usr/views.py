from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from app.models import Tickets
from django.http import HttpResponseRedirect
from mailer import send_mail
from django.conf import settings
# from django.urls import reverse 

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    return render(response, 'usr/dashboard.html',{})

@login_required(login_url='/login/')
def my_tickets(response):
    open_tickets = Tickets.objects.filter(is_closed=None,user=response.user)
    closed_tkts = Tickets.objects.filter(is_closed=True,user=response.user)

    return render(response, 'usr/tickets.html',{'open_tickets':open_tickets,'closed_tkts':closed_tkts})    

@login_required(login_url='/login/')
def file_a_ticket(response):
    if response.method == "POST":
        form = TicketForm(response.POST or None)
        if form.is_valid():
            tickets = form.save(commit=False)
            tickets.user = response.user
            tickets.save()

            send_mail(
                'Ticket Filed',
                'Your Ticket has been issued. You can check in the app for recent updates.',
                settings.DEFAULT_FROM_EMAIL,
                [tickets.user.email],
                fail_silently=False,
            )
            return redirect('/dashboard/my_tickets/')
    else:
        form=TicketForm()
    args = {'form': form}

    return render(response, 'usr/file_a_ticket.html',args)