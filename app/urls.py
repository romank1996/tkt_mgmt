from django.urls import path

from app import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.signedin, name='signedin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_faq', views.CreateFaq.as_view(), name='create_faq'),
]