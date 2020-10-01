from app.models import TicketStatusHistory
import datetime
from django.core import mail
from app.models import Status
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.models import User

def change_status(ticket, user, comment):
    ticketHistory = TicketStatusHistory()
    ticketHistory.status=ticket.status
    ticketHistory.ticket_id=ticket.ticket_id
    ticketHistory.change_time=datetime.datetime.now()
    ticketHistory.modified_by=user
    ticketHistory.comment=comment
    ticketHistory.save()

    sync_to_async(email_notification(ticket, False))



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
    
    mail.send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        to_emails,
        fail_silently=True,
    )
    