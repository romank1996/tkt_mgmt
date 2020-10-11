from django.urls import path, include

from adm import views

app_name='admin_app'
urlpatterns = [
    # path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='admin_dashboard'),
    path('dashboard/tickets/', views.tickets, name='admin_tickets'),
    path('dashboard/tickets/create_new_ticket/', views.create_new_ticket, name='create_new_ticket'),
    path('tickets/assign_tickets/<int:pk>', views.assign_tickets, name='assign_tickets'),
    path('dashboard/reports/', views.reports, name='admin_reports'),
    # path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('report-form-chart/', views.report_form_data, name='report-form-chart'),
    path('report-form/', views.report_form, name='report-form'),
]