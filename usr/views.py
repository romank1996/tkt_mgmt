from app.models import Tickets, TicketStatusHistory
from bootstrap_modal_forms.generic import BSModalReadView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from app import notification
from .forms import TicketForm
import datetime
# from django.urls import reverse 

# Create your views here.
@login_required(login_url='/login/')
def index(response):
    open_tickets = Tickets.objects.filter((Q(is_closed=None) | Q(is_closed = False)),user=response.user).count()
    closed_tkts = Tickets.objects.filter(is_closed=True,user=response.user).count()
    return render(response, 'usr/dashboard.html',{'new':open_tickets,'complete':closed_tkts})

@login_required(login_url='/login/')
def my_tickets(response):
    open_tickets = Tickets.objects.filter((Q(is_closed=None) | Q(is_closed = False)),user=response.user)
    closed_tkts = Tickets.objects.filter(is_closed=True,user=response.user)
    return render(response, 'usr/tickets.html',{'open_tickets':open_tickets,'closed_tkts':closed_tkts})    

@login_required(login_url='/login/')
def file_a_ticket(response):
    if response.method == "POST":
        form = TicketForm(response.POST or None)
        if form.is_valid():
            tickets = form.save(commit=False)
            tickets.user = response.user
            tickets.created_at = datetime.datetime.now()
            tickets.save()

            notification.email_notification(tickets, True)

            return redirect('/dashboard/my_tickets/')
    else:
        form=TicketForm()
    args = {'form': form}

    return render(response, 'usr/file_a_ticket.html',args)

class TicketDetailView(BSModalReadView):
    model = Tickets
    template_name='usr/ticket_detail.html'

def view_history(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        pk = request.GET.get("pk", None)
        data = TicketStatusHistory.objects.filter(ticket_id=pk)
        if not data:
            return JsonResponse({'data':'valid'}, status = 400)
        serialized_data = serializers.serialize( "json", data)
        return JsonResponse(serialized_data, status = 200,safe=False)

    return JsonResponse({}, status = 400)
