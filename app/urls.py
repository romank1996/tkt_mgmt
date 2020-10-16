from django.urls import path

from app import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.signedin, name='signedin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_faq', views.CreateFaq.as_view(), name='create_faq'),
    path('detail_faq/<int:pk>', views.DetailFaq.as_view(), name='detail_faq'),
    path('edit_faq/<int:pk>', views.UpdateFaq.as_view(), name='edit_faq'),
    path('faq/<int:pk>/remove', views.DeleteFaq.as_view(), name='faq_remove'),
    path('chat/', views.get_chat_data, name='get_chat_data'),
    path('send_message/', views.send_message, name='send_message'),
]