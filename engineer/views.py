from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Tickets,Status, TicketStatusHistory
from app import notification
from django.http import JsonResponse
from django.contrib.auth.models import User
import datetime

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


# for report form
from .forms import ReportFormEng

def report_form_data_eng(request):
    user_group = [group.name for group in request.user.groups.all()]

    if request.method == 'POST':
        form = ReportFormEng(request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            # print(username, date_from, date_to)
            # print(type(date_from))

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

            return render(request, 'engineer/pie_chart_eng.html', {
                'labels': labels,
                'data': data,
    })

    else:
        form = ReportFormEng()
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
        if date_from < match_val.change_time and match_val.change_time <= date_to:
            count = count + 1
    return count

def find_overdue_no(queryset, date_from, date_to):
    ticket_ids = [tkt_id.pk for tkt_id in queryset]
    count = 0
    for ticket_id in ticket_ids:
        match_val = TicketStatusHistory.objects.filter(ticket_id=ticket_id)
        match_val = match_val.order_by('-change_time')[0]
        finish_date = Tickets.objects.get(pk=ticket_id).finish_date
        if date_from < match_val.change_time and match_val.change_time <= date_to and finish_date < datetime.date.today():
            count = count + 1
    return count
