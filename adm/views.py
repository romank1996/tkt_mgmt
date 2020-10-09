import datetime

from app import notification
from app.models import (Status, TicketAssignHistory, Tickets,
                        TicketStatusHistory)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView, UpdateView
import json
from django.core.serializers import serialize
from .forms import TicketAssignForm, TicketForm
import adm.admin_reports as admin_reports

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    new_tickets = Tickets.objects.filter((Q(is_closed=None) | Q(is_closed = False)),assigned_to=None).count()
    overdue = Tickets.objects.filter((Q(is_closed=None) | Q(is_closed = False)), finish_date__lt = datetime.datetime.today()).count()
    complete = Tickets.objects.filter(status=Status.objects.get(status='Complete')).count()
    # data = (['Ticket Status','Number of Tickets'],['New Tickets',new_tickets],['Assigned Tickets',assigned],['Inprogress',working_on],['Completed',complete])
    data = admin_reports.ticket_counts
    line_data = admin_reports.ticketStatus
    return render(response, 'adm/dashboard.html',{'new':new_tickets,'overdue':overdue,'complete':complete, 'data':data, 'line_data':line_data})

@login_required(login_url='/login/')
def tickets(response):
    new_tickets = Tickets.objects.filter((Q(is_closed=None) | Q(is_closed = False)),assigned_to=None).order_by('ticket_id')
    assigned = Tickets.objects.filter(status=Status.objects.get(status='Assigned'))
    working_on = Tickets.objects.filter(status=Status.objects.get(status='Inprogress'))
    complete = Tickets.objects.filter(status=Status.objects.get(status='Complete'))

    args = {
        'new_tickets':new_tickets,
        'assigned':assigned,
        'working_on':working_on,
        'complete':complete
    }
    return render(response, 'adm/admin_tickets.html',args)


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

@login_required(login_url='/login/')
def assign_tickets(response, pk):
    ticket = Tickets.objects.get(ticket_id=pk)
    userInfo = User.objects.get(username=ticket.user)
    form = TicketAssignForm(response.POST or None, instance=ticket)

    if response.method == "POST":
        if form.is_valid():
            tickets = form.save(commit=False)
            ticket.priority = tickets.priority
            ticket.finish_date = tickets.finish_date
            ticket.assigned_to = tickets.assigned_to
            ticket.assigned_at = datetime.datetime.now()
            ticket.status = Status.objects.get(status='Assigned')
            ticket.save()

            notification.change_status(ticket, response.user, 'Ticket is Assigned')
            
            assignHistory=TicketAssignHistory(ticket_id=ticket.ticket_id,assigned_to=tickets.assigned_to,assigned_time=datetime.datetime.now(),assigned_by=response.user)
            assignHistory.save()
            
            return redirect('/dashboard/tickets')

    args = {'form': form,'userInfo':userInfo, 'ticket':ticket}

    return render(response, 'adm/assign_tickets.html',args)


def reports(response):
    data = admin_reports.ticketStatus
    args={
        'data':data
    }
    return render(response,'adm/report.html', args)