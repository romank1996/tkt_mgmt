from django.db import models
from django.contrib import admin
from app.models import Tickets,TicketStatusHistory
from django.forms import inlineformset_factory
# Create your models here.



# class TicketStatisHistoryInLine(admin.TabularInline):
#     model = TicketStatusHistory

# class TicketAdmin(admin.ModelAdmin):
#     inlines = [
#         TicketStatisHistoryInLine,
#     ]