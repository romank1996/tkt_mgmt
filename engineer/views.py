from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Tickets,Status
from app import status_change
from django.http import JsonResponse

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


def start_working(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        pk = request.GET.get("pk", None)
        ticket = Tickets.objects.filter(ticket_id=pk).first()
        ticket.status = Status.objects.get(status='Inprogress')
        ticket.save()
        status_change.change_status(ticket,request.user,'Started Working on Ticket')

        return JsonResponse({'data': 'success'}, status = 200)

    return JsonResponse({}, status = 400)