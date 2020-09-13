from django.urls import path

from adm import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/tickets/', views.tickets, name='dashboard/admin_tickets'),
    path('dashboard/tickets/create_new_ticket/', views.create_new_ticket, name='create_new_ticket'),
]