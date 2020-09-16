from django.urls import path

from engineer import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/ticket_list/', views.ticket_list, name='dashboard/ticket_list'),
    # path('dashboard/ticket_list/file_a_ticket/', views.file_a_ticket, name='file_a_ticket'),
]