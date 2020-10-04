from django.urls import path
from django.conf.urls import url
from usr import views

app_name = "user_tickets"
urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/my_tickets/', views.my_tickets, name='dashboard/my_tickets'),
    path('dashboard/my_tickets/file_a_ticket/', views.file_a_ticket, name='file_a_ticket'),
    path('ticket_details/<int:pk>', views.TicketDetailView.as_view(), name='ticket_details'),
    path('view_history/', views.view_history, name='view_history'),
]