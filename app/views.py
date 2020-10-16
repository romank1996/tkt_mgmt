from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Faqs, Message, Conversation, Tickets
from django.urls import reverse, reverse_lazy
from adm import views as admin_views
from engineer import views as engineer_views
from usr import views as user_views
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from app import notification

def index(response):
    return render(response, "app/base.html", {})

def faq(response):
    faqs = Faqs.objects.all()
    return render(response,"app/faq.html", {"list":faqs} )

def home(response):
    return render(response, "app/home.html", {})

def signedin(response):
    group = response.user.groups.filter(user=response.user)[0]
    if group.name=="user":
        return user_views.index(response)
    elif group.name=="engineer":
        return engineer_views.index(response)
    elif group.name=="admin":
        return admin_views.index(response)

def dashboard(response):
    return render(response, "app/dashboard.html")

def base_template(request):
    context={}
    if request.user.is_authenticated and not request.user.is_superuser:
        user_group = request.user.groups.all()[0].name
        if user_group == 'user':
            context = {'base_template_name': 'usr/usr_dash.html'}
        elif user_group == 'admin':
            context = {'base_template_name': 'adm/admin_sidenav.html'}
        elif user_group == 'engineer':
            context = {'base_template_name': 'engineer/eng_sidenav.html'}
    
    if request.user.is_authenticated and request.user.is_superuser:
        context = {'base_template_name': 'adm/admin_sidenav.html'}
    return context


# CBV for FAQs
class CreateFaq(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Faqs
    fields = ('question', 'answer')


class DetailFaq(DetailView):
    login_url = '/accounts/login/'
    model = Faqs


class UpdateFaq(LoginRequiredMixin, UpdateView):
    model = Faqs
    fields = ('question', 'answer')


class DeleteFaq(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Faqs
    success_url = reverse_lazy('faq')

#chat
def get_chat_data(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        pk = request.GET.get("pk", None)
        con = Conversation.objects.filter(ticket=pk).first()
        if not con:
            return JsonResponse({'data':'No Conversation Yet','status':'201'}, status = 201)
        messages = Message.objects.filter(conversation=con).order_by('date_time').all()
        data = []
        for item in messages:
            is_user = True if item.sender == request.user else False 
            formatedDate = item.date_time.strftime("%m-%d %H:%M")
            data.append({'sender':item.sender_name, 'message': item.message,'date_time': formatedDate,'is_user': is_user})
        # serialized_data = serializers.serialize( "json", data)
        return JsonResponse(data, status = 200,safe=False)

    return JsonResponse({}, status = 400)

#chat
def send_message(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        pk = request.GET.get("pk", None)
        message = request.GET.get("message", None)
        try:
            con = notification.save_conversation(pk)
            notification.save_message(con, request.user, message)
            return JsonResponse({'data':'success'}, status = 200)
        except Exception as e:
            return JsonResponse({'data':'fail'}, status = 400)
    return JsonResponse({}, status = 400)

