from app.models import Tickets, TicketStatusHistory,Status
from django.db.models import Count
from django.core.serializers import serialize
import datetime
import json
from django.db import connection

def ticketStatus():
    raw_query = (
        "select DISTINCT(date(t.created_at)) as date,  count(t.ticket_id) as created, 0 as completed  from tickets t "
        " where date(t.created_at) > current_date - interval '30' day"
        " group by t.created_at"
        " union"
        " select DISTINCT(date(ts.change_time)) as date, 0 as created, count(ts.id) as completed  from ticket_status_history ts"
        " where ts.status_id = 3 and (date(ts.change_time) > current_date - interval '30' day)"
        " group by ts.change_time ;"
    )
    cursor = connection.cursor()

    cursor.execute(raw_query)
    data = cursor.fetchall()


    return json.dumps(list(data),indent=4, sort_keys=True, default=str)


def ticket_counts():
    raw_query = (
        "select 0 status,count(t.ticket_id) as new, 0 assigned,0 inprogress,0 complete,0 cancelled from tickets t" 
        " WHERE t.assigned_to is NULL and date(t.created_at) > current_date - interval '30' day"
        " union"
        " select ts.status_id,"
        " 0,"
        " sum(case when status_id=1 then 1 else 0 end) as assigned,"
        " sum(case when status_id=2 then 1 else 0 end) as inprogress,"
        " sum(case when status_id=3 then 1 else 0 end) as complete,"
        " sum(case when status_id=5 then 1 else 0 end) as cancelled"
        " from ticket_status_history ts"
        " WHERE  date(ts.change_time) > current_date - interval '30' day"
        " group by ts.status_id;"
   )
    cursor = connection.cursor()

    cursor.execute(raw_query)
    data = cursor.fetchall()

    pie_data = []
    # pie_data.append(['Ticket Status','Number of Tickets'])

    for item in data:
        tkt_status = 'New Tickets'
        tkt_num = 0
        if item[0] == 1:
            tkt_status = 'Assigned'
            tkt_num = item[2]
        elif item[0] == 2:
            tkt_status = 'Inprogress'
            tkt_num = item[3]
        elif item[0] == 3:
            tkt_status = "Complete"
            tkt_num = item[4]
        elif item[0] == 5:
            tkt_status = "Cancelled"
            tkt_num = item[5]
        elif item[0] == 0:
            tkt_num = item[1]

        pie_data.append([tkt_status,tkt_num])

    return json.dumps(list(pie_data),indent=4, sort_keys=True, default=str)