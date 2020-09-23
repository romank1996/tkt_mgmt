from django.urls import path
from django.conf.urls import url
from usr import views

app_name = 'usr_app'
urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/my_tickets/', views.my_tickets, name='dashboard/my_tickets'),
    path('dashboard/my_tickets/file_a_ticket/', views.file_a_ticket, name='file_a_ticket'),
    path('dashboard/my_tickets/view/<int:pk>', views.TicketView.as_view(), name='view_ticket'),
    url(r'^dashboard/my_tickets/view_history/$', views.TicketHistoryView, name='view_history'),
]