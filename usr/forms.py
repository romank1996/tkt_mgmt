from django import forms
from .models import Tickets

class TicketForm(forms.ModelForm):

    class Meta:
        model = Tickets
        fields = ["issue_type", "description", "priority"]
