from django.shortcuts import render,redirect
from django.views.generic import UpdateView, ListView
from django.contrib.auth.decorators import login_required
from app.models import Tickets,Status,TicketStatusHistory,TicketAssignHistory
from .forms import TicketForm,TicketAssignForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime
from django.contrib.auth.models import User
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


# class TicketAssignView(UpdateView):
#     model = Tickets
#     form_class = TicketForm
#     template_name = 'adm/assign_tickets.html'

#     def dispatch(self, **kwargs):
#         self.ticket_id = kwargs['pk']
#         return super(TicketAssignView, self).dispatch(**kwargs)

#     def form_valid(self, form):
#         form.save()
#         ticket = Tickets.objects.get(ticket_id=self.ticket_id)
#         return HttpResponse(render_to_string('adm/assign_tickets_success.html', {'ticket': ticket}))

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

            ticketHistory = TicketStatusHistory()
            ticketHistory.status_id=ticket.status.status_id
            ticketHistory.ticket_id=ticket
            ticketHistory.change_time=datetime.datetime.now()
            ticketHistory.modified_by=response.user
            ticketHistory.comment="Ticket is Assigned"
            ticketHistory.save()
            
            assignHistory=TicketAssignHistory(ticket_id=ticket.ticket_id,assigned_to=tickets.assigned_to,assigned_time=datetime.datetime.now(),assigned_by=response.user)
            assignHistory.save()
            
            return redirect('/dashboard/tickets')

    args = {'form': form,'userInfo':userInfo, 'ticket':ticket}

    return render(response, 'adm/assign_tickets.html',args)
