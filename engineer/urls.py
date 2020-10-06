from django.urls import path

from engineer import views

app_name = "engineer_app"
urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/ticket_list/', views.ticket_list, name='eng_ticket_list'),
    path('confirmation/', views.start_working, name='start_working_confirm'),
    path('confirmation/close_tkt', views.close_ticket, name='close_ticket'),
    path('dashboard/engineers_list', views.engineers_list, name='engineers_list'),
    path('change_active_status/<int:pk>', views.change_active_status, name='change_active_status'),
]