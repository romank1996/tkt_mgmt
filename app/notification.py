from app.models import TicketStatusHistory,Conversation,Message,Tickets
import datetime
from django.core import mail
from app.models import Status
from django.conf import settings
from django.contrib.auth.models import User
from background_task import background
from django.core.management import call_command

def change_status(ticket, user, comment):
    ticketHistory = TicketStatusHistory()
    ticketHistory.status=ticket.status
    ticketHistory.ticket_id=ticket.ticket_id
    ticketHistory.change_time=datetime.datetime.now()
    ticketHistory.modified_by=user
    ticketHistory.comment=comment
    ticketHistory.save()

    email_notification(ticket, False)

def email_notification(ticket, is_new):
    subject = 'Ticket Status Update'
    message = 'Ticket status has been changed. Please check the website for detail.'
    to_emails = [ticket.user.profile.email]
    ticket_id = str(ticket.ticket_id)
    if(is_new):
        subject = 'Ticket Filed'
        message = ('Your Ticket #' + ticket_id + ' has been successfully Created.' +
        'Please visit website to view further details or to create new Ticket. Thank You.')
        users = User.objects.filter(groups__name='admin').all()
        for user in users:
            to_emails.append(user.profile.email)


    if ticket.status == Status.objects.get(status='Complete'):
        subject = 'Ticket Closed'
        message = ('Your Ticket #' + ticket_id + ' has been successfully closed.' +
        'Please visit website to view further details or to create new Ticket. Thank You.')

    if ticket.status == Status.objects.get(status='Assigned'):
        subject = 'Ticket Assigned'
        message = ('Ticket #' + ticket_id + ' has been Assigned to '+ ticket.assigned_to.username + '.' +
        'Please visit website to view further details. Thank You.')
        to_emails.append(ticket.assigned_to.profile.email)

    if ticket.status == Status.objects.get(status='Inprogress'):
        message = ('Status of Ticket #' + ticket_id + ' has been updated.' +
        'Please visit website to view further details. Thank You.')
    
    send_nodification.now(subject,message,to_emails)

@background(schedule=30)
def send_nodification(subject,message,to_emails):

    mail.send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        to_emails,
        fail_silently=True,
    )

def save_conversation(tkt_id):
    data = Conversation.objects.filter(ticket=tkt_id).first()
    if not data:
        con = Conversation()
        con.ticket = (0 if tkt_id == 0 else Tickets.objects.filter(ticket_id=tkt_id).first())
        con.title = 'Ticket #' + str(tkt_id)
        con.created = datetime.datetime.now()
        con.save()
        return con

    return data

def save_message(conv, sender, message):
    mess = Message()
    mess.conversation = conv
    mess.sender = sender
    mess.message = message
    mess.date_time = datetime.datetime.now()
    mess.save()

