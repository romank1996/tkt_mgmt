from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Tickets,Status
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    return render(response, 'engineer/dashboard.html',{})

@login_required(login_url='/login/')
def ticket_list(response):
    new_tickets = Tickets.objects.filter(status=Status.objects.get(status='Assigned'),assigned_to=response.user)
    working_on = Tickets.objects.filter(status=Status.objects.get(status='Inprogress'),assigned_to=response.user)
    complete = Tickets.objects.filter(status=Status.objects.get(status='Complete'),assigned_to=response.user)
    unassigned = Tickets.objects.filter(status=None,assigned_to=None)

    args = {
        'new_tickets':new_tickets,
        'working_on':working_on,
        'complete':complete,
        'unassigned':unassigned
    }
    return render(response, 'engineer/tickets_list.html',args)

@login_required(login_url='/login/')
def engineers_list(response):
    active_engineers = User.objects.filter(groups__name='engineer', is_active=True)
    inactive_engineers = User.objects.filter(groups__name='engineer', is_active=False)

    args = {
        'active_engineers': active_engineers,
        'inactive_engineers': inactive_engineers
    }

    return render(response, 'engineer/engineers_list.html', args)