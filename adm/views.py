import datetime

from app import notification
from app.models import (Status, Tickets,
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
from django.db.models import Sum
from django.http import JsonResponse

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
                        
            return redirect('/dashboard/tickets')

    args = {'form': form,'userInfo':userInfo, 'ticket':ticket}

    return render(response, 'adm/assign_tickets.html',args)


def reports(response):
    data = admin_reports.ticketStatus
    args={
        'data':data
    }
    return render(response,'adm/report.html', args)
# for report form
from .forms import ReportForm
from django.http import HttpResponseRedirect

def report_form(response):
    return render(response, 'adm/report_form.html')

def report_form_data(request):
    user_group = [group.name for group in request.user.groups.all()]

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            print(username, date_from, date_to)
            print(type(date_from))

            labels = ["Completed", "In Progress", "Overdue"]
            data = []
            if 'admin' in user_group:
                engineer_id = User.objects.get(username=username).id
            elif 'engineer' in user_group:
                engineer_id = request.user.id
            else:
                print("not accessible")
            
            queryset = Tickets.objects.filter(assigned_to__exact=engineer_id)

            complete_queryset = queryset.filter(status__status='Complete')
            no_of_completed_tickets = find_no(complete_queryset, date_from, date_to)
            print("no of completed tickets", no_of_completed_tickets)
            data.append(no_of_completed_tickets)

            inprogress_queryset = queryset.filter(status__status='Inprogress')
            no_of_inprogress_tickets = find_no(inprogress_queryset, date_from, date_to)
            print("no of inprogress tickets", no_of_inprogress_tickets)
            data.append(no_of_inprogress_tickets)

            overdue_queryset = queryset.filter(status__status='Inprogress')
            no_of_overdue_tickets = find_overdue_no(overdue_queryset, date_from, date_to)
            print("no of overdue tickets", no_of_overdue_tickets)
            data.append(no_of_overdue_tickets)

            return render(request, 'adm/pie_chart.html', {
                'labels': labels,
                'data': data,
                'username': username,
    })

    else:
        form = ReportForm()
    if 'admin' in user_group:
        return render(request, 'adm/report_form.html', {'form': form})
    else:
        return render(request, 'engineer/report_form_eng.html', {'form': form})
    

def find_no(queryset, date_from, date_to):
    ticket_ids = [tkt_id.pk for tkt_id in queryset]
    count = 0
    for ticket_id in ticket_ids:
        match_val = TicketStatusHistory.objects.filter(ticket_id=ticket_id)
        match_val = match_val.order_by('-change_time')[0]
        if date_from <= match_val.change_time and match_val.change_time <= date_to:
            count = count + 1
    return count

def find_overdue_no(queryset, date_from, date_to):
    ticket_ids = [tkt_id.pk for tkt_id in queryset]
    count = 0
    for ticket_id in ticket_ids:
        match_val = TicketStatusHistory.objects.filter(ticket_id=ticket_id)
        match_val = match_val.order_by('-change_time')[0]
        finish_date = Tickets.objects.get(pk=ticket_id).finish_date
        if date_from <= match_val.change_time and match_val.change_time <= date_to and finish_date < datetime.date.today():
            count = count + 1
    return count
