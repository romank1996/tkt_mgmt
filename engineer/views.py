from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Tickets,Status
from app import notification
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
# Create your views here.
@login_required(login_url='/login/')
def index(response):
    assined_status = status=Status.objects.get(status='Assigned')
    inprogress_status = status=Status.objects.get(status='Inprogress')
    new_tickets = Tickets.objects.filter(status=Status.objects.get(status='Assigned'),assigned_to=response.user).count()
    overdue = Tickets.objects.filter((Q(status=assined_status) | Q(status = inprogress_status)), finish_date__lt = datetime.datetime.today(),assigned_to=response.user).count()
    complete = Tickets.objects.filter(status=Status.objects.get(status='Complete'),assigned_to=response.user).count()

    return render(response, 'engineer/dashboard.html',{'new':new_tickets,'overdue':overdue,'complete':complete})

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


def start_working(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        pk = request.GET.get("pk", None)
        ticket = Tickets.objects.filter(ticket_id=pk).first()
        ticket.status = Status.objects.get(status='Inprogress')
        ticket.save()
        notification.change_status(ticket,request.user,'Started Working on Ticket')

        return JsonResponse({'data': 'success'}, status = 200)

    return JsonResponse({}, status = 400)


def close_ticket(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        pk = request.GET.get("pk", None)
        comment = request.GET.get("comment", None)
        ticket = Tickets.objects.filter(ticket_id=pk).first()
        ticket.status = Status.objects.get(status='Complete')
        ticket.is_closed = True
        ticket.save()
        notification.change_status(ticket,request.user,('Ticket has been successfully closed.' if comment == '' else comment))

        return JsonResponse({'data': 'success'}, status = 200)

    return JsonResponse({}, status = 400)
    
@login_required(login_url='/login/')
def engineers_list(response):
    active_engineers = User.objects.filter(groups__name='engineer', is_active=True)
    inactive_engineers = User.objects.filter(groups__name='engineer', is_active=False)

    args = {
        'active_engineers': active_engineers,
        'inactive_engineers': inactive_engineers
    }

    return render(response, 'engineer/engineers_list.html', args)
