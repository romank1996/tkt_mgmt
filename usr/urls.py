from django.urls import path

from usr import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/my_tickets/', views.my_tickets, name='dashboard/my_tickets'),
    path('dashboard/my_tickets/file_a_ticket/', views.file_a_ticket, name='file_a_ticket'),
]