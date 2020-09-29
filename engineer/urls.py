from django.urls import path

from engineer import views

app_name = "engineer_app"
urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/ticket_list/', views.ticket_list, name='eng_ticket_list'),
    path('confirmation/', views.start_working, name='start_working_confirm'),
    # path('dashboard/ticket_list/file_a_ticket/', views.file_a_ticket, name='file_a_ticket'),
]