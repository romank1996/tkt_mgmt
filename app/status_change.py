from app.models import TicketStatusHistory
import datetime

def change_status(ticket, user, comment):
    ticketHistory = TicketStatusHistory()
    ticketHistory.status=ticket.status
    ticketHistory.ticket_id=ticket.ticket_id
    ticketHistory.change_time=datetime.datetime.now()
    ticketHistory.modified_by=user
    ticketHistory.comment=comment
    ticketHistory.save()